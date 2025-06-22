from fastapp.app.repository.userRepo import UserRepository
from fastapp.app.schema.user import UserOutput, UserInCreate, UserInUpdate, UserWithToken
from fastapp.app.security.hash import Hash
from fastapp.app.security.authH import AuthH
from sqlalchemy.orm import Session
from fastapi import HTTPException


class UserService:
    def __init__(self, session: Session):
        self.__userRepository = UserRepository(session=session)

    def register(self, user_detail: UserInCreate)->UserOutput:
        if self.__userRepository.user_be_by_email(email=user_detail.email):
            raise HTTPException(status_code=400, detail="Email занят")

        hashed_password = Hash.get_password_hash(plain_password=user_detail.password)
        user_detail.password = hashed_password
        return self.__userRepository.create_user(user_date=user_detail)

    def login(self, login_detail: UserInCreate)->UserWithToken:
        if not self.__userRepository.user_be_by_email(email=login_detail.email):
            raise HTTPException(status_code=404, detail="Email не зарегистрирован")

        user = self.__userRepository.get_user_by_email(email=login_detail.email)
        if Hash.verify_password(plain_password=login_detail.password, hashed_password=user.password):
            token = AuthH.encode_jwt(user_id=user.id, role=user.role)
            if token:
                return UserWithToken(token=token)
            raise HTTPException(status_code=500, detail="request")

        raise HTTPException(status_code=400, detail="Неверный логин и пароль")

    def get_user_by_id(self, user_id: int):
        user = self.__userRepository.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=400, detail="User not available")