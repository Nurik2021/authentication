from http.client import HTTPException

from fastapi import APIRouter, FastAPI
from fastapi.params import Depends
from fastapp.app.schema.user import UserInLogin, UserInCreate, UserInUpdate, UserWithToken, UserOutput
from sqlalchemy.orm import Session
from fastapp.app.core.database import get_db
from fastapp.app.security.authH import AuthH
from fastapp.app.service.userService import UserService



authRouter = APIRouter()

# adminRouter = APIRouter()

@authRouter.post('/login', status_code= 200, response_model=UserWithToken)
def login(loginDetails: UserInLogin, session: Session=Depends(get_db)):
    try:
        return UserService(session=session).login(login_detail=loginDetails)
    except Exception as error:
        print(error)
        raise error

@authRouter.post('/register', status_code= 201, response_model=UserOutput)
def register(registerDetails: UserInCreate, session: Session=Depends(get_db)):
    try:
        return UserService(session=session).register(user_detail=registerDetails)
    except Exception as error:
        print(error)
        raise error
    return {'date': registerDetails}

# @adminRouter.post("/login",status_code= 201, response_model=UserWithToken)
# async def admin_login(login_detail: UserInLogin, session: Session=Depends(get_db)):
#     auth_service = UserService()
#     user_with_token = auth_service.login(login_detail)  # Авторизация
#
#     # Декодируем токен, чтобы проверить роль
#     user_data = AuthH.decode_jwt(user_with_token.token)
#     if user_data.get("role") != "admin":
#         raise HTTPException(status_code=403, detail="Только администраторы могут входить в админку")
#
#     return user_with_token