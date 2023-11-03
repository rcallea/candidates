# from operator import and_
# from fastapi import APIRouter, Depends, status
# from src.models import models
# from src.schemas.response import ResponseDto
# from src.schemas.schemas import Employee
# from sqlalchemy.orm import Session
# from src.database import get_db
# from fastapi.encoders import jsonable_encoder

# router = APIRouter()

# @router.get("/{company_id}/projects/{project_id}/employees", response_model=ResponseDto, status_code=status.HTTP_200_OK)
# def get_employees(company_id:int, project_id:int, db: Session = Depends(get_db)):
#     project = db.query(models.Project).filter(models.Project.id == project_id).first()
#     project_employees = [
#         employee
#         for employee in project.employees
#         if employee.employee.company_id == company_id
#     ]
    
#     employees = [{
#         "employee": project_employee.employee,
#         "position": project_employee.position
#     } for project_employee in project_employees]

#     return {"message":f"all employees in company {company_id} and project {project_id}","data":jsonable_encoder(employees),"errors":""}

# @router.post("/{company_id}/projects/{project_id}/employees", response_model=ResponseDto, status_code=status.HTTP_200_OK)
# async def post_employee_to_project(company_id:int, project_id:int, payload: Employee, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.identification == payload.identification).first()  
    if not employee:
        employee = models.Employee(
            company_id=company_id,
            identification= payload.identification,
            identification_type=payload.identification_type,
            name=payload.name,
            surname=payload.surname,
            phone=payload.phone
        )
        db.add(employee)
        db.commit()
        db.refresh(employee)
    
    project_employe = db.query(models.ProjectEmployee)\
                        .filter(and_(models.ProjectEmployee.employee_id == employee.id, 
                                     models.ProjectEmployee.project_id == project_id))\
                        .first()

    if not project_employe:
        project_employe = models.ProjectEmployee(
            employee_id=employee.id,
            project_id=project_id,
            position=payload.position
        )
        db.add(project_employe)
        db.commit()
        db.refresh(project_employe)

    return {"message":f"Employee added for proyect id: {project_id} ","data":jsonable_encoder(employee),"errors":""}