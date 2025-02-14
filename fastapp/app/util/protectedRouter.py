from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated, Union
from fastapp.app.security.authH import AuthH
from fastapp.app.service.userService import UserService
from fastapp.app.core.database import get_db
from fastapp.app.schema.user import UserOutput

AUTH_PREFIX = 'Bearer '


def get_current_user(
        session: Session = Depends(get_db),
        authorization: Annotated[Union[str, None], Header()] = None
) -> UserOutput:
    print(f"Authorization header: {authorization}")
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid Authentication Credentials"
    )

    if not authorization:
        print("Authorization header is missing")
        raise auth_exception

    if not authorization.startswith(AUTH_PREFIX):
        print("Authorization header does not start with 'Bearer '")
        raise auth_exception

    payload = AuthH.decode_jwt(token=authorization[len(AUTH_PREFIX):])

    if payload and payload["user_id"]:
        try:
            user = UserService(session=session).get_user_by_id(payload["user_id"])
            return UserOutput(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                role=user.role,


            )
        except Exception as error:
            raise error
    raise auth_exception

def get_admin_user(user: UserOutput = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Access denied")
    return user
