from flask import request
from manage_airline.models import User, Airport, FlightSchedule, BetweenAirport
from manage_airline import db
import hashlib
import datetime
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


def get_airport(a_id):
    return Airport.query.filter(Airport.id.__eq__(a_id)).all()[0]


def get_airport_json(a_id):
    a = get_airport(a_id)
    return {
        'id': a.id,
        'name': a.name
    }


def get_airport_bw_list(f_id):
    return BetweenAirport.query.filter(BetweenAirport.flight_sche_id.__eq__(f_id)).all()


def get_airport_bw_list_json(f_id):
    bwa_list = BetweenAirport.query.filter(BetweenAirport.flight_sche_id.__eq__(f_id))
    airport_between_list = []
    for bwa in bwa_list:
        obj = {
            'id': bwa.id,
            'airport': get_airport_json(bwa.airport_id),
            'flight_sche': bwa.flight_sche_id,
            'time_stay': bwa.time_stay,
            'note': bwa.note
        }
        airport_between_list.append(obj)
    return airport_between_list


def get_flight_sche_list(active=False):
    f_list = FlightSchedule.query.filter(FlightSchedule.is_active.__eq__(active))
    flight_sche_list = []
    for f in f_list:
        flight_sche = get_flight_sche(f.id)
        flight_sche_list.append(flight_sche)
    return flight_sche_list


def get_flight_sche(f_id):
    f = FlightSchedule.query.filter(FlightSchedule.id.__eq__(f_id)).all()[0]
    bwa_list = get_airport_bw_list_json(f.id)
    af = get_airport_json(f.airport_from)
    at = get_airport_json(f.airport_to)
    return {
        'id': f.id,
        'airport_from': af,
        'airport_to': at,
        'is_active': f.is_active,
        'time_start': f.time_start,
        'time_end': f.time_end,
        'quantity_ticket_1st': f.quantity_ticket_1st,
        'quantity_ticket_1st_booked': f.quantity_ticket_1st_booked,
        'quantity_ticket_2nd': f.quantity_ticket_2nd,
        'quantity_ticket_2nd_booked': f.quantity_ticket_2nd_booked,
        'price': f.price,
        'airport_between_list': {
            'quantity': len(bwa_list),
            'data': bwa_list
        }
    }


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


def search_flight_schedule(ap_from, ap_to, time_start, ticket_type):
    time_arr = time_start.split('-')
    time = datetime.datetime(int(time_arr[0]), int(time_arr[1]), int(time_arr[2]))

    f_list = FlightSchedule.query.filter(FlightSchedule.is_active.__eq__(True))
    f_list = f_list.filter(FlightSchedule.airport_from.__eq__(ap_from),
                           FlightSchedule.airport_to.__eq__(ap_to),
                           FlightSchedule.time_start.__gt__(time))

    if ticket_type == 1:
        f_list.filter(FlightSchedule.quantity_ticket_1st.__gt__(FlightSchedule.quantity_ticket_1st_booked))
    if ticket_type == 2:
        f_list.filter(FlightSchedule.quantity_ticket_2nd.__gt__(FlightSchedule.quantity_ticket_2nd_booked))

    flight_sche_list = []
    for f in f_list:
        flight_sche = get_flight_sche(f.id)
        flight_sche_list.append(flight_sche)
    return flight_sche_list


if __name__ == '__main__':
    from manage_airline import app

    with app.app_context():
        print(get_flight_sche(2))
