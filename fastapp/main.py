from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapp.app.util.init_db import create_tables
from fastapp.app.routers.auth import authRouter
from fastapp.app.util.protectedRouter import get_current_user
from fastapp.app.schema.user import UserOutput
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router=authRouter, tags=["auth"], prefix="/auth")
#/auth/login

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://192.168.87.54:8000"],  # Разрешаем все источники (лучше указать точные домены)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки, включая Authorization
)



@app.get("/dashboard")
async def dashboard():
    return {"status": "Добро пожаловать"}

@app.get("/protected")
async def read_protected(user: UserOutput = Depends(get_current_user)):
    return user
# @app.get("/admin")
# async def admin_dashboard(admin: UserOutput = Depends(get_admin_user)):
#     return {"message": admin}