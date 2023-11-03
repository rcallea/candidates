from pydantic import BaseModel
from typing import Optional, Union
from enum import Enum

class ResponseDto(BaseModel):
    message: str
    data: Union[list, dict, str]
    errors: str 

class AcademicLevel(str, Enum):
    UNDERGRADUATE = "PREGRADO"
    SPECIALIZATION = "ESPECIALIZACIÓN"
    MASTER = "MAESTRÍA"
    DOCTORATE = "DOCTORADO"
    DIPLOMAT = "DIPLOMADO"
    COURSE = "CURSO"
    CERTIFICATION = "CERTIFICACIÓN"

class StateEducation(str, Enum):
    IN_PROGRESS = "EN CURSO"
    FINALIZED = "FINALIZADO"
    CANCELLED = "CANCELADO"
    POSTPONED = "APLAZADO"
    SLOPE_GRADE = "PENDIENTE GRADO"

class LanguageLevel(str, Enum):
    A0 = "A0"
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

class EmploymentType(str, Enum):
    FULL_TIME = "JORNADA COMPLETA"
    PART_TIME = "JORNADA PARCIAL"
    TEMPORAL_AGREEMENT = "CONTRATO TEMPORAL"
    INDEPENDENT  = "PROFESIONAL INDEPENDIENTE"
    PRACTICES = "CONTRATO DE PRÁCTICAS"

class Candidate(BaseModel):
    full_name: str
    surnames: str
    age: str
    document_type: str
    document: str
    phone: str
    birthdate: str
    country: str
    city: str
    email: str
    address: str

class CandidateUpdate(BaseModel):
    full_name: Optional[str] = None
    surnames: Optional[str] = None
    age: Optional[str] = None
    document_type: Optional[str] = None
    document: Optional[str] = None
    phone: Optional[str] = None
    birthdate: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    email: Optional[str] = None
    address: Optional[str] = None

class Language(BaseModel):
    pass

class Education(BaseModel):
    start_date: str
    end_date: Optional[str] = None
    title: str
    educational_institution: str
    degree: AcademicLevel
    state: StateEducation
    candidate_id: str

class EducationUpdate(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    title: Optional[str] = None
    educational_institution: Optional[str] = None
    degree: Optional[str] = None
    state: Optional[str] = None 

class WorkExperience(BaseModel):
    company: str
    job_title: str
    start_date: str
    end_date: Optional[str] = None
    functions: str
    job_type: EmploymentType
    is_actual: bool
    candidate_id: int

class WorkExperienceUpdate(BaseModel):
    company: Optional[str] = None 
    job_title: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    functions: Optional[str] = None
    job_type: Optional[EmploymentType] = None
    is_actual: Optional[bool] = None

class Profile(BaseModel):
    curriculum: Optional[str] = None
    description: Optional[str] = None
    candidate_id: int

class SkillsUpdate(BaseModel):
    description: Optional[str] = None
    soft_skills: Optional[list] = None
    technical_skills: Optional[list] = None
    personality_traits: Optional[list] = None