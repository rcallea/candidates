from src.routes import ping, candidates, languages, educations, workexperiences, profiles, enums
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from src.database import engine, SessionLocal
from src.models import models

models.Base.metadata.create_all(bind = engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    app.state.db = SessionLocal()

@app.on_event("shutdown")
async def shutdown_db_client():
    app.state.db.close()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        openapi_version="3.0.0",
        title="api-candidates",
        version="1.0.0",
        description="Microservices Candidates",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema
app.openapi = custom_openapi

prefix_microservice = "/api/candidates"
app.include_router(ping.router, tags=["healthcheck"], prefix=f'{prefix_microservice}/ping')
app.include_router(candidates.router, tags=["candidates"], prefix=f"{prefix_microservice}")
app.include_router(languages.router, tags=["languages"], prefix=f"{prefix_microservice}/languages")
app.include_router(educations.router, tags=["educations"], prefix=f"{prefix_microservice}/educations")
app.include_router(workexperiences.router, tags=["workexperiences"], prefix=f"{prefix_microservice}/workexperiences")
app.include_router(profiles.router, tags=["profiles"], prefix=f"{prefix_microservice}/profiles")
app.include_router(enums.router, tags=["enums"], prefix=f"{prefix_microservice}/enums")