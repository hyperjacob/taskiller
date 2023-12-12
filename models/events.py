# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, Integer, ForeignKey, Boolean, String, DateTime
# импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref

# импортируем модель пользователей для связки моделей
from models.users import Users
from data_base.dbcore import Base


class Events(Base):
    """
    Класс для создания таблицы "события",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'events'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    create_at = Column(DateTime)
    period = Column(Integer) # 1 - один раз, 3 - раз в неделю, 4 - раз в месяц, 5 - раз в год
    icon = Column(String)
    name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    # для каскадного удаления данных из таблицы
    users = relationship(
        Users,
        backref=backref('events',
                        uselist=True,
                        cascade='delete,all'))

