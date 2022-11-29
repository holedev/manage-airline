from flask import Flask
from urllib.parse import quote
import cloudinary
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


app.secret_key = 'secret-key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/it01saledbv2?charset=utf8mb4' % quote('Admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)

cloudinary.config(cloud_name='by1410', api_key='334579152917615', api_secret='_zqF24Mo-9RIE3bryU-KzJ1ACBU')


