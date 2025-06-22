import jwt
import time

from decouple import config

JWT_SECRET = config('JWT_SECRET')
JWT_ALGORITHM = config('JWT_ALGORITHM')



class AuthH(object):

    @staticmethod
    def encode_jwt(user_id: int, role:str):
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': time.time() + 3600
        }

        token = jwt.encode(payload,  JWT_SECRET, algorithm=JWT_ALGORITHM)
        return token


    @staticmethod
    def decode_jwt(token):
        try:
            decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            return decoded_token if decoded_token["exp"] >= time.time() else None
        except:
            print("ошибка декод токена")