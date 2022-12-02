from manage_airline import app, db
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from manage_airline.models import UserRole, User

admin = Admin(app=app, name='Quản lý', template_mode='bootstrap4')


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


admin.add_view(AuthenticatedModelView(User, db.session, name="Người dùng"))
