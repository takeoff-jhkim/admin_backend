from fastapi import FastAPI
from app.routers import admin
from app.database import engine, Base
from fastapi.middleware.cors import CORSMiddleware

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(admin.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 개발용으로 전체 허용. 운영에서는 도메인 제한하기
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)