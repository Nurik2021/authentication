from sqladmin import ModelView
from fastapp.app.user.models import User

class UserAdmin(ModelView, model=User):
    column_list = [User.email,User.phone_number,User.role, User.first_name, User.last_name ]
    can_create = False
    can_export = False
    name_plural = "Пользователи"
    category = "User"
    column_searchable_list = [User.email]
    column_labels = {User.email: "Почта",
                     User.phone_number: "Телефон",
                     User.role: "Тип пользователя",
                     User.first_name: "Имя",
                     User.last_name: "Фамилия"}


