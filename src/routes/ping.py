from fastapi import APIRouter
from src.schemas import schemas

router = APIRouter()

@router.get("", response_model=schemas.ResponseDto)
def healthcheck():
    return schemas.ResponseDto(message = "pong", data = "", errors ="")