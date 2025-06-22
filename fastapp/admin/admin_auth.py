from typing import Any, Coroutine

from fastapi import Request, HTTPException, Form
from sqladmin.authentication import AuthenticationBackend
from starlette.responses import RedirectResponse
import httpx

from fastapp.app.core.database import get_db
from fastapp.app.security.authH import AuthH
from fastapp.app.service.userService import UserService
from fastapp.app.util.protectedRouter import get_admin_user  # Функция проверки роли

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        # 1. Получаем данные из формы (SQLAdmin отправляет form-data)
        form = await request.form()
        email = form.get("username")  # SQLAdmin использует поле "username"
        password = form.get("password")

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "http://127.0.0.1:8000/auth/login",  # URL вашего API
                    json={
                        "email": email,
                        "password": password
                    },
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()  # Проверка статуса ответа
                token_data = response.json()

                user_data = AuthH.decode_jwt(token_data["token"])
                if user_data.get("role") != "admin":
                    return False  # Если роль не "admin", запрещаем вход

                # 3. Сохраняем токен в сессии
                request.session.update({
                    "token": token_data["token"],
                    "user_id": AuthH.decode_jwt(token_data["token"])["user_id"]
                })
                return True

            except httpx.HTTPStatusError as e:
                # Обработка ошибок аутентификации
                if e.response.status_code == 401:
                    return False  # Неверные логин/пароль

                elif e.response.status_code == 422:
                    print("Ошибка 422:", e.response.json())  # Логируем причину ошибки
                    return False  # Возвращаем False, чтобы показать ошибку в аутентификации
                elif e.response.status_code == 404:
                    print("Ошибка 404:", e.response.json())  # Логируем причину ошибки
                    return False  # Возвращаем False, чтобы показать ошибку в аутентификации
                elif e.response.status_code == 500:
                    print("Ошибка 500:", e.response.json())  # Логируем причину ошибки
                    return False  # Возвращаем False, чтобы показать ошибку в аутентификации

                raise e  # Если это другая ошибка, выбрасываем исключение

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> RedirectResponse | bool:
        token = request.session.get("token")
        if not token:
            return RedirectResponse(url="/admin/login")

        try:
            # Декодируем токен, чтобы получить объект пользователя
            user_data = AuthH.decode_jwt(token)

            # Проверяем роль
            if user_data.get("role") != "admin":
                raise HTTPException(status_code=403, detail="Доступ запрещён")

            return True
        except HTTPException:
            return RedirectResponse(url="/admin/login")