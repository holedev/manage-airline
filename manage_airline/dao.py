from flask import request
from manage_airline.models import User, Airport, FlightSchedule, BetweenAirport
from manage_airline import db
import hashlib
import google.auth.transport.requests
from pip._vendor import cachecontrol
import requests
from manage_airline import flow
from google.oauth2 import id_token
import os
from dotenv import load_dotenv
load_dotenv()


def get_user_by_id(user_id):
    return User.query.get(user_id)


def register(fullname, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(fullname=fullname, username=username.strip(), password=password)
    db.session.add(u)
    db.session.commit()


def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def get_user_oauth():
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    user_oauth = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=os.getenv("OAUTH_CLIENT_ID")
    )
    return user_oauth


def get_airport_list():
    return Airport.query.filter().all()


def get_flight_sche_list():
    return FlightSchedule.query.filter().all()


def create_flight_sche(airport_from, airport_to, time_start, time_end, quantity_ticket_1st, quantity_ticket_2nd):
    f = FlightSchedule(airport_from=airport_from, airport_to=airport_to, time_start=time_start,
                       time_end=time_end, quantity_ticket_1st=quantity_ticket_1st,
                       quantity_ticket_2nd=quantity_ticket_2nd)
    db.session.add(f)
    db.session.commit()
    return f


def create_bwa(airport_id, flight_sche_id, time_stay, note):
    bwa = BetweenAirport(airport_id=airport_id, flight_sche_id=flight_sche_id, time_stay=time_stay, note=note)
    db.session.add(bwa)
    db.session.commit()
    return bwa
