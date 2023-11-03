from fastapi import APIRouter, Depends, status
from src.database import get_db
from src.models import models
# from sqlalchemy.orm import Session
# from src.schemas.response import ResponseDto
# from src.schemas.schemas import Project
from fastapi.encoders import jsonable_encoder

router = APIRouter()

# @router.get("/{company_id}/projects", response_model=ResponseDto, status_code=status.HTTP_200_OK)
# async def get_projects(company_id:int, db: Session = Depends(get_db)):
#     projects = db.query(models.Project).filter(models.Project.company_id == company_id).all()
#     return {"message":f"all projects for company with id: {company_id}","data":jsonable_encoder(projects),"errors":""}

# @router.post("/{company_id}/projects", response_model=ResponseDto, status_code=status.HTTP_200_OK)
# async def create_project(company_id:int, payload: Project, db: Session = Depends(get_db)):
#     project = models.Project(company_id=company_id,
#                              name=payload.name,
#                              description=payload.description,
#                              start_date = payload.start_date
#                             )

#     db.add(project)
#     db.commit()
#     db.refresh(project)

#     return {"message":f"project added for company id: {company_id} ","data":jsonable_encoder(project),"errors":""}