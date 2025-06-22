from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from fastapp.admin.admin_auth import AdminAuth
from fastapp.admin.views import UserAdmin
from fastapp.app.core.database import engine
from fastapp.app.routers import flights, orders
from fastapp.app.util.init_db import create_tables
from fastapp.app.routers.auth import authRouter
from fastapp.app.util.protectedRouter import get_current_user, get_admin_user
from fastapp.app.schema.user import UserOutput
from sqladmin import Admin
from decouple import config



JWT_SECRET = config('JWT_SECRET')








@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

app = FastAPI(lifespan=lifespan)
# app.include_router(router=adminRouter, tags=["admin"], prefix="/admin")

app.include_router(router=authRouter, tags=["auth"], prefix="/auth")
#/auth/login

authentication_backend = AdminAuth(secret_key=JWT_SECRET)
admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UserAdmin)

app.include_router(flights.router, prefix="/flights")

app.include_router(orders.router, prefix="/orders")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешаем все источники (лучше указать точные домены)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы
    allow_headers=["*"],  # Разрешаем все заголовки, включая Authorization
)

@app.get("/users/profile")
async def read_users_profile(user: UserOutput = Depends(get_current_user)):
    return user



@app.get("/dashboard")
async def dashboard():
    return {"status": "Добро пожаловать"}

@app.get("/protected")
async def read_protected(user: UserOutput = Depends(get_current_user)):
    return user
# @app.get("/admin")
# async def admin_dashboard(admin: UserOutput = Depends(get_admin_user)):
#     return admin