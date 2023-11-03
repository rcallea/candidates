# from fastapi import APIRouter, Depends, status
# from src.database import get_db
# from src.models import models
# from sqlalchemy.orm import Session
# from src.schemas.response import ResponseDto
# from fastapi.encoders import jsonable_encoder

# router = APIRouter()

# @router.get("/{company_id}", response_model=ResponseDto, status_code=status.HTTP_200_OK)
# async def get_company(company_id:int, db: Session = Depends(get_db)):
#     company = db.query(models.Company).filter(models.Company.id == company_id).first()

#     company_data = jsonable_encoder(company)
#     company_data["employees"] = [jsonable_encoder(employee) for employee in company.employees]
#     company_data["projects"] = [jsonable_encoder(project) for project in company.projects]        

#     return {"message":f"details for company {company_id}","data":jsonable_encoder(company),"errors":""}
    
