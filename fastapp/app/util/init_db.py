
from fastapp.app.core.database import Base, engine


def create_tables():
    Base.metadata.create_all(bind=engine)  # Создаем таблицы в базе данных