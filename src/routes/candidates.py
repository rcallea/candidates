from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from src.logic.profiles import get_candidates_profiles
from src.models import models
from src.schemas import schemas
from sqlalchemy.orm import Session, attributes
from src.database import get_db
from fastapi.encoders import jsonable_encoder
import requests
import ast

router = APIRouter()

SKILLS_URL = "http://a48085841837c4e16a907ae6d6147724-1134772844.us-east-1.elb.amazonaws.com"

@router.get("", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def get_candidates(soft_skills:str=None, technical_skills:str=None, personality_traits:str=None, db:Session = Depends(get_db)):    
    if not soft_skills and not technical_skills and not personality_traits: 
        candidates = db.query(models.Candidate).all()
        return schemas.ResponseDto(message = "all candidates by skills", data = jsonable_encoder(candidates), errors ="")
    
    skills = {
       "soft_skills": ast.literal_eval(soft_skills.replace(" ", "")) if soft_skills else [],
       "technical_skills": ast.literal_eval(technical_skills.replace(" ", "")) if technical_skills else [],
       "personality_traits": ast.literal_eval(personality_traits.replace(" ", "")) if personality_traits else []
    }
    
    profiles = get_candidates_profiles(skills)
    candidates = db.query(models.Candidate)\
                   .filter(models.Candidate.profiles.any(models.Profile.id.in_(profiles)))\
                   .all()
    
    return schemas.ResponseDto(message = "all candidates by skills", data = jsonable_encoder(candidates), errors ="")

@router.get("/{candidate_id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def get_candidates(candidate_id:int, db: Session = Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    
    if not candidate:
        return JSONResponse(content={"message": "FAILED", "data":candidate, "errors":""}, status_code=404) 
    
    info_candidate = candidate.__dict__

    languages_data = db.query(models.Lenguage).filter(models.Lenguage.candidate_id == candidate_id).all()
    info_candidate['languages'] = languages_data if languages_data else []
            
    profile_data = db.query(models.Profile).filter(models.Profile.candidate_id == candidate_id).first()
    
    if profile_data:
        attributes_dict = attributes.instance_dict(profile_data)
        profile_data = {**attributes_dict}
        skills_response = requests.get(f"{SKILLS_URL}/api/profiles/{profile_data['id']}/candidates/skills")
        
        if skills_response.status_code == 200:
            skills = skills_response.json()
            profile_data['soft_skills'] = skills['data']['soft_skills']
            profile_data['technical_skills'] = skills['data']['technical_skills'] 
            profile_data['personality_traits'] = skills['data']['personality_traits']
        
        info_candidate['profile'] = profile_data

    else:    
        info_candidate['profile'] = []

    education_data = db.query(models.Education).filter(models.Education.candidate_id == candidate_id).all()
    info_candidate['educations'] = education_data if education_data else []

    workexperience_data = db.query(models.WorkExperience).filter(models.WorkExperience.candidate_id == candidate_id).all()
    info_candidate['workexperiences'] = workexperience_data if workexperience_data else []

    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(info_candidate) , errors ="") 

@router.post("", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def create_candidate(payload: schemas.Candidate, db: Session=Depends(get_db)):
    candidate = db.query(models.Candidate).filter(models.Candidate.document == payload.document).first()
   
    if candidate:
       return JSONResponse(content={"message": "FAILED", "data":"", "errors":"Candidato ya registrado"}, status_code=210) 
    
    candidate = db.query(models.Candidate).filter(models.Candidate.email == payload.email).first()
    if candidate:
       return JSONResponse(content={"message": "FAILED", "data":"", "errors":"Email ya registrado"}, status_code=210) 

    db_candidate = models.Candidate(
                                    full_name       = payload.full_name, 
                                    surnames        = payload.surnames,
                                    age             = payload.age,
                                    document_type   = payload.document_type,
                                    document        = payload.document,
                                    phone           = payload.phone,
                                    birthdate       = payload.birthdate, 
                                    country         = payload.country,
                                    city            = payload.city,
                                    email           = payload.email,
                                    address         = payload.address
                                    ) 
    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)
    
    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(db_candidate) , errors ="") 

@router.put("/{candidate_id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def put_candidate(candidate_id:int, payload: schemas.CandidateUpdate, db: Session=Depends(get_db)):
    db_candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    candidate_data = payload.model_dump(exclude_none=True)

    if db_candidate is None:
        return JSONResponse(content={"message": "SUCCESS", "data":"", "errors":"Candidato no encontrado"}, status_code=404) 
    
    for key, value in candidate_data.items():
        setattr(db_candidate, key, value)
    
    db.commit()
    db.refresh(db_candidate)

    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(db_candidate) , errors ="")

@router.put("/{candidate_id}/skills", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def put_candidate_skills(candidate_id:int, payload: schemas.SkillsUpdate, db: Session=Depends(get_db)):
    db_candidate = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    candidate_data = payload.model_dump(exclude_none=True)

    db_profile_candidate = db.query(models.Profile).filter(models.Profile.candidate_id == candidate_id).first()

    if db_profile_candidate:
        if db_candidate is None:
            return JSONResponse(content={"message": "FAILED", "data":"", "errors":"Candidato no encontrado"}, status_code=404) 

        if candidate_data.get("description"): 
            setattr(db_profile_candidate, "description", candidate_data['description'])
            db.commit()
        
        if candidate_data.get('soft_skills'):
            post_json = { "candidate_id": candidate_id, "personality_traits":candidate_data['personality_traits'], "soft_skills":candidate_data['soft_skills'], "technical_skills":candidate_data['technical_skills'] }
            skills_response = requests.post(f"{SKILLS_URL}/api/profiles/{db_profile_candidate.id}/candidates/skills", json=post_json)
            if skills_response.status_code == 200:
                return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(candidate_data) , errors ="")
        
        return schemas.ResponseDto(message = "FAILED", data = "" , errors ="Error al actualizar habilidades")
    
    create_profile = models.Profile(
                                curriculum = "", 
                                description = candidate_data['description'],
                                candidate_id    = candidate_id
                                ) 
    db.add(create_profile)
    db.commit()
    db.refresh(create_profile)

    post_json = { "candidate_id": candidate_id, "personality_traits":candidate_data['personality_traits'], "soft_skills":candidate_data['soft_skills'], "technical_skills":candidate_data['technical_skills'] }
    skills_response = requests.post(f"{SKILLS_URL}/api/profiles/{create_profile.id}/candidates/skills", json=post_json)
    if skills_response.status_code == 200:
        return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(candidate_data) , errors ="")
        
    return schemas.ResponseDto(message = "FAILED", data = "" , errors ="Error al actualizar habilidades")