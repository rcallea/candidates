from fastapi import APIRouter, HTTPException, Depends, status
from src.models import models
from src.schemas import schemas
from sqlalchemy.orm import Session
from src.database import get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter()

@router.get("/{candidate_id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
def get_educations(candidate_id:int, db: Session = Depends(get_db)):
    educations = db.query(models.Education).filter(models.Education.candidate_id == candidate_id).order_by(models.Education.id.desc()).all()

    if educations is None:
        return schemas.ResponseDto(message = "FAILED", data = "" , errors ="Educación no encontrada") 
    
    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(educations) , errors ="")

@router.post("", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def create_education(payload: schemas.Education, db: Session=Depends(get_db)):
    db_education = models.Education(
                                    start_date              = payload.start_date, 
                                    end_date                = payload.end_date,
                                    title                   = payload.title,
                                    educational_institution = payload.educational_institution,
                                    degree                  = payload.degree,
                                    state                   = payload.state,
                                    candidate_id            = payload.candidate_id
                                    ) 
    db.add(db_education)
    db.commit()
    db.refresh(db_education)
    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(db_education) , errors ="")

@router.put("/{id}", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def put_educations(id:str, payload: schemas.EducationUpdate, db: Session=Depends(get_db)):
    db_education = db.query(models.Education).filter(models.Education.id == id).first()

    data = payload.model_dump(exclude_none=True)

    if db_education is None:
        raise HTTPException(status_code=404, detail="Educación no encontrado")
    
    for key, value in data.items():
        setattr(db_education, key, value)

    db.commit()
    db.refresh(db_education)

    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(db_education) , errors ="")