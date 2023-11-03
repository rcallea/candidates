from fastapi import APIRouter, Depends, status, Request
from src.models import models
from src.schemas import schemas
from sqlalchemy.orm import Session
from src.database import SessionLocal, get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
def get_language(db: Session = Depends(get_db)):
    languages = db.query(models.Lenguage).all()
    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(languages) , errors ="") 

@router.get("/{id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
def get_language(id:str, db: Session = Depends(get_db)):
    language = db.query(models.Lenguage).filter(models.Lenguage.candidate_id == id).all()
    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(language) , errors ="") 

@router.post("", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def create_language(request: Request, language: schemas.Language, db: Session=Depends(get_db)):
    data = await request.json()
    db_language = models.Lenguage(
                                    language        = data['language'], 
                                    language_level   = data['language_level'],
                                    candidate_id    = data['candidate_id']
                                    ) 
    db.add(db_language)
    db.commit()
    db.refresh(db_language)

    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(db_language) , errors ="") 


@router.put("/{id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def put_language(id:str, payload: schemas.WorkExperienceUpdate, db: Session=Depends(get_db)):
    return schemas.ResponseDto(message = "SUCCESS", data = "" , errors ="") 
