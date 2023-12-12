# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, DateTime
# импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref

# импортируем модель пользователей для связки моделей
from models.users import Users
from models.tasks import Tasks
from data_base.dbcore import Base


class Bufertask(Base):
    """
    Класс для создания таблицы "события",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'bufertask'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    task_id = Column(Integer)
    user_id = Column(Integer)



