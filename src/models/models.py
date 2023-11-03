from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
from src.database import Base
import enum

class LanguageLevel(str,enum.Enum):
    A0 = "A0"
    A1 = "A1"
    A2 = "A2"
    B1 = "B1"
    B2 = "B2"
    C1 = "C1"
    C2 = "C2"

class EmploymentType(str,enum.Enum):
    FULL_TIME = "JORNADA COMPLETA"
    PART_TIME = "JORNADA PARCIAL"
    TEMPORAL_AGREEMENT = "CONTRATO TEMPORAL"
    INDEPENDENT  = "PROFESIONAL INDEPENDIENTE"
    PRACTICES = "CONTRATO DE PRACTICAS"

class AcademicLevel(str,enum.Enum):
    UNDERGRADUATE = "PREGRADO"
    SPECIALIZATION = "ESPECIALIZACIÓN"
    MASTER = "MAESTRÍA"
    DOCTORATE = "DOCTORADO"
    DIPLOMAT = "DIPLOMADO"
    COURSE = "CURSO"
    CERTIFICATION = "CERTIFICACION"

class StateEducation(str,enum.Enum):
    IN_PROGRESS = "EN CURSO"
    FINALIZED = "FINALIZADO"
    CANCELLED = "CANCELADO"
    POSTPONED = "APLAZADO"
    SLOPE_GRADE = "PENDIENTE GRADO"

class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    surnames = Column(String)
    age = Column(Integer)
    document_type = Column(String)
    document = Column(String)
    phone = Column(String)
    birthdate = Column(Date())
    country = Column(String)
    city = Column(String)
    email = Column(String)
    address = Column(String)

    languages = relationship("Lenguage", back_populates="candidate")
    educations = relationship("Education", back_populates="candidate")
    workexperiences = relationship("WorkExperience", back_populates="candidate")
    profiles = relationship("Profile", back_populates="candidate")

    __table_args__ = ({"schema": "candidates"},)

class Lenguage(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True, index=True)
    language = Column(String)
    language_level = Column(Enum(LanguageLevel), index=True)

    candidate_id = Column(Integer, ForeignKey("candidates.candidates.id"))
    candidate = relationship("Candidate", back_populates="languages")

    __table_args__ = ({"schema": "candidates"},)

class Education(Base):
    __tablename__ = "educations"
    id = Column(Integer, primary_key=True, index=True)
    start_date = Column(Date())
    end_date = Column(Date())
    title = Column(String)
    educational_institution = Column(String)
    degree = Column(Enum(AcademicLevel), index=True)
    state = Column(Enum(StateEducation), index=True)

    candidate_id = Column(Integer, ForeignKey("candidates.candidates.id"))
    candidate = relationship("Candidate", back_populates="educations")

    __table_args__ = ({"schema": "candidates"},) 

class WorkExperience(Base):
    __tablename__ = "work_experiences"
    id = Column(Integer, primary_key=True, index=True)
    company = Column(String)
    job_title = Column(String)
    start_date = Column(Date())
    end_date = Column(Date())
    functions = Column(String)
    job_type = Column(Enum(EmploymentType), index=True)
    is_actual = Column(Boolean, default=False)

    candidate_id = Column(Integer, ForeignKey("candidates.candidates.id"))
    candidate = relationship("Candidate", back_populates="workexperiences")

    __table_args__ = ({"schema": "candidates"},)

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    curriculum = Column(String)
    description = Column(String)

    candidate_id = Column(Integer, ForeignKey("candidates.candidates.id"))
    candidate = relationship("Candidate", back_populates="profiles")

    __table_args__ = ({"schema": "candidates"},) 