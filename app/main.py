from fastapi import FastAPI
from .routers import admin
from .database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(admin.router)