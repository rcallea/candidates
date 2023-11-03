from fastapi import APIRouter, HTTPException, Depends, status
from src.models import models
from src.schemas import schemas
from sqlalchemy.orm import Session
from src.database import get_db
from fastapi.encoders import jsonable_encoder
import datetime

router = APIRouter()

@router.get("/{candidate_id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
def get_workexperiences(candidate_id:int, db: Session = Depends(get_db)):
    workexperiences = db.query(models.WorkExperience).filter(models.WorkExperience.candidate_id == candidate_id).order_by(models.WorkExperience.id.desc()).all()

    if not workexperiences:
        return schemas.ResponseDto(message = "FAILED", data = "" , errors ="") 
    
    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(workexperiences) , errors ="") 

def es_fecha_valida(fecha_str):
    try:
        datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@router.post("", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def create_workexperiences(payload: schemas.WorkExperience, db: Session=Depends(get_db)):
        
    db_workexperience = models.WorkExperience(
                                    company      = payload.company, 
                                    job_title    = payload.job_title,
                                    start_date   = payload.start_date,
                                    end_date     = payload.end_date,
                                    functions    = payload.functions,
                                    job_type     = payload.job_type,
                                    is_actual    = payload.is_actual,
                                    candidate_id = payload.candidate_id
                                    ) 
    
    db.add(db_workexperience)
    db.commit()
    db.refresh(db_workexperience)
    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(db_workexperience) , errors ="") 

@router.put("/{id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def put_workexperience(id:str, payload: schemas.WorkExperienceUpdate, db: Session=Depends(get_db)):
    db_workexperience = db.query(models.WorkExperience).filter(models.WorkExperience.id == id).first()

    data = payload.model_dump(exclude_none=True)

    if db_workexperience is None:
        raise HTTPException(status_code=404, detail="Experiencia no encontrada")
    
    for key, value in data.items():
        setattr(db_workexperience, key, value)

    db.commit()
    db.refresh(db_workexperience)

    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(db_workexperience) , errors ="")