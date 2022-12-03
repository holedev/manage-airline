from flask import request
from manage_airline.models import User
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
