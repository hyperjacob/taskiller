# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, DateTime
# импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref

# импортируем модель пользователей для связки моделей
from models.users import Users
from data_base.dbcore import Base


class Inbox(Base):
    """
    Класс для создания таблицы "входящие",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'inbox'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    message = Column(String)
    url = Column(String, default="")
    is_active = Column(Boolean)
    user_id = Column(Integer, ForeignKey('users.id'))
    # для каскадного удаления данных из таблицы
    users = relationship(
        Users,
        backref=backref('inbox',
                        uselist=True,
                        cascade='delete,all'))

