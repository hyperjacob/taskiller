from sqlalchemy import Column, String, Integer, Boolean, DateTime
from data_base.dbcore import Base
from datetime import datetime


class Users(Base):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    teleid = Column(String)
    is_activ = Column(Boolean)
    last_login = Column(DateTime, default=datetime.now())


    def __str__(self):
        return self.name
