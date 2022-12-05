from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Enum, DateTime
from enum import Enum as UserEnum
from manage_airline import db, app
from flask_login import UserMixin
import hashlib

default_password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2
    STAFF = 3


class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)


class User(BaseModel, UserMixin):
    fullname = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), default=default_password)
    image = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.name


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # u = User(fullname='ADMIN', username='admin', password=password, user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()

        pass
