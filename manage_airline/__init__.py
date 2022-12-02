import os

from flask import Flask
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager
from flask_babelex import Babel
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)


app.secret_key = os.getenv('SECRET_KEY')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/%s?charset=utf8mb4'\
                                        % (quote(os.getenv('PW_DB')), os.getenv('NAME_DB'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

login = LoginManager(app=app)

cloudinary.config(cloud_name=os.getenv('CLOUDINARY_NAME'),
                  api_key=os.getenv('CLOUDINARY_API_KEY'),
                  api_secret=os.getenv('CLOUDINARY_API_SECRET'))

babel = Babel(app=app)


@babel.localeselector
def load_locale():
    return 'vi'
