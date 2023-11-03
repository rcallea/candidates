from fastapi import APIRouter, HTTPException, Depends, status, Request
from src.models import models
from src.schemas import schemas
from sqlalchemy.orm import Session
from src.database import SessionLocal, get_db
from fastapi.encoders import jsonable_encoder


router = APIRouter()
   
@router.get("", response_model=schemas.ResponseDto, status_code=status.HTTP_200_OK)
async def get_enums(db: Session = Depends(get_db)):
    response =  {
        "language_level": {level.value for level in models.LanguageLevel},
        "employment_type": {type.value for type in models.EmploymentType},
        "academic_level": {level.value for level in models.AcademicLevel},
        "state_education": {state.value for state in models.StateEducation},
    }

    return schemas.ResponseDto(message = "SUCCESS", data = jsonable_encoder(response) , errors ="") 