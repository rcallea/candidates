from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from src.models import models
from src.schemas import schemas
from sqlalchemy.orm import Session
from src.database import get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter()
   
@router.get("", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def get_profilesx(db: Session = Depends(get_db)):
    #profiles = db.query(models.Profile).all()
    return schemas.ResponseDto(message = "SUCCESS", data = "", errors ="")

# @router.get("/{candidate_id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
# async def get_profile(candidate_id:int=None, db: Session = Depends(get_db)):
#     profiles = db.query(models.Profile).filter(models.Profile.candidate_id == candidate_id).all()

#     if not profiles:
#         response_error =  jsonable_encoder(schemas.ResponseDto(message = "FAILED", data = "" , errors ="Not found"))
#         return JSONResponse(content=response_error, status_code=404)
    
#     return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(profiles) , errors ="")     

@router.post("", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def create_profile(request: Request, profiles: schemas.Profile, db: Session=Depends(get_db)):
    data = await request.json()
    db_profile = models.Profile(
                                curriculum = data['curriculum'], 
                                description = data['description'],
                                candidate_id    = data['candidate_id']
                                ) 
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(db_profile) , errors ="") 

@router.put("/{id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def put_profiles(id:int, request: Request, profiles: schemas.Profile, db: Session=Depends(get_db)):
    db_profiles = db.query(models.Profile).filter(models.Profile.id == id).first()

    data = await request.json()

    if db_profiles is None:
        raise HTTPException(status_code=404, detail="Candidato no encontrado")
    
    for key, value in data.items():
        setattr(db_profiles, key, value)

    db.commit()
    data['id'] = id

    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(data) , errors ="") 