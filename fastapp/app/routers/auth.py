from fastapi import APIRouter
from fastapi.params import Depends
from fastapp.app.schema.user import UserInLogin, UserInCreate, UserInUpdate, UserWithToken, UserOutput
from sqlalchemy.orm import Session
from fastapp.app.core.database import get_db
from fastapp.app.service.userService import UserService

authRouter = APIRouter()


authRouter = APIRouter()


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