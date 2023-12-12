# компоненты библиотеки для описания структуры таблицы
from sqlalchemy import Column, Integer, ForeignKey
# импортируем модуль для связки таблиц
from sqlalchemy.orm import relationship, backref

# импортируем модель пользователей для связки моделей
from models.users import Users
from data_base.dbcore import Base


class Stats(Base):
    """
    Класс для создания таблицы "статистика",
    основан на декларативном стиле SQLAlchemy
    """
    # название таблицы
    __tablename__ = 'stats'

    # поля таблицы
    id = Column(Integer, primary_key=True)
    uts = Column(Integer)

    user_id = Column(Integer, ForeignKey('users.id'))
    # для каскадного удаления данных из таблицы
    users = relationship(
        Users,
        backref=backref('stats',
                        uselist=True,
                        cascade='delete,all'))

    def __repr__(self):
        """
        Метод возвращает формальное строковое представление указанного объекта
        """
        return f"{self.score} {self.games} {self.trys} {self.tips}"
