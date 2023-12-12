# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, DateTime
# импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref

# импортируем модель пользователей для связки моделей
from models.users import Users
from data_base.dbcore import Base


class Folders(Base):
    """
    Класс для создания таблицы "входящие",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'folders'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    name = Column(String)
    id_type = Column(Integer)
    is_active = Column(Boolean)
    icon = Column(String)
    teg = Column(String)
    friend = Column(String)
    access_lvl = Column(Integer)
    user_id = Column(Integer, ForeignKey('users.id'))
    # для каскадного удаления данных из таблицы
    users = relationship(
        Users,
        backref=backref('folders',
                        uselist=True,
                        cascade='delete,all'))

    def __str__(self):
        return self.name

