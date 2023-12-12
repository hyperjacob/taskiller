# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, DateTime
# импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref

# импортируем модель пользователей для связки моделей
from models.folders import Folders
from data_base.dbcore import Base


class Tasks(Base):
    """
    Класс для создания таблицы "входящие",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'tasks'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    is_active = Column(Boolean)
    last_touch = Column(DateTime)
    untill = Column(DateTime)
    icon = Column(String)
    name = Column(String)
    folder_id = Column(Integer, ForeignKey('folders.id'))
    # для каскадного удаления данных из таблицы
    folders = relationship(
        Folders,
        backref=backref('tasks',
                        uselist=True,
                        cascade='delete,all'))

