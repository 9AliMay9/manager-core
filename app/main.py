from fastapi import FastAPI

from app import models
from app.database import engine
from app.routes import sbj, obj


# Initialize Fastapi app
app = FastAPI()


# Root route for testing
@app.get("/")
def read_root():
    return {"message": '"2x4" Entity API ready'}


# Register routers
app.include_router(sbj.router)
app.include_router(obj.router)
