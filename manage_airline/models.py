from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, Enum, DateTime, Time
from enum import Enum as UserEnum
from sqlalchemy.orm import relationship, backref
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
        return self.fullname


class Airport(BaseModel):
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class FlightSchedule(BaseModel):
    __tablename__ = 'flight_sche'

    airport_from = Column(Integer, ForeignKey(Airport.id))
    airport_to = Column(Integer, ForeignKey(Airport.id))
    is_active = Column(Boolean, default=False)
    time_start = Column(DateTime, nullable=False)
    time_end = Column(DateTime, nullable=False)
    quantity_ticket_1st = Column(Integer, nullable=False)
    quantity_ticket_1st_booked = Column(Integer, default=0)
    quantity_ticket_2nd = Column(Integer, nullable=False)
    quantity_ticket_2nd_booked = Column(Integer, default=0)
    price = Column(Integer, default=0)

    bw_airports = relationship('BetweenAirport', backref='flight_sche', lazy=False)

    def __str__(self):
        return str(self.id)


class BetweenAirport(BaseModel):
    __tablename__ = 'between_airport'

    airport_id = Column(Integer, ForeignKey(Airport.id))
    flight_sche_id = Column(Integer, ForeignKey(FlightSchedule.id))
    time_stay = Column(Integer, nullable=False)
    note = Column(String(100))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # u = User(fullname='ADMIN', username='admin', password=password, user_role=UserRole.ADMIN)
        # db.session.add(u)
        # db.session.commit()

        pass
