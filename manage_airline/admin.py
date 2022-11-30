from manage_airline import app
from flask_admin import Admin

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app=app, name='QUẢN TRỊ BÁN HÀNG', template_mode='bootstrap4')