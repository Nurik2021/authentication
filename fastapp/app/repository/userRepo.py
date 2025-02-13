from typing import Type

from .base import BaseRepository
from fastapp.app.user.models import User
from fastapp.app.schema.user import UserInCreate

class UserRepository(BaseRepository):
    def create_user(self, user_date: UserInCreate):
        newUser = User(**user_date.model_dump(exclude_none=True))

        self.session.add(instance=newUser)
        self.session.commit()
        self.session.refresh(instance=newUser)

        return newUser
    def user_be_by_email(self, email: str)->bool:
        user = self.session.query(User).filter_by(email=email).first()
        return bool(user)
    def get_user_by_email(self, email: str)-> Type[User] | None:
        user = self.session.query(User).filter_by(email=email).first()
        return user
    def get_user_by_id(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user