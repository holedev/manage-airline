from flask import redirect, url_for

from manage_airline import app, db
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from manage_airline.models import UserRole, User


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class UserView(AuthenticatedModelView):
    form_excluded_columns = ['password']


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect('/login')
        if not current_user.user_role == UserRole.ADMIN:
            return redirect('/')
        return self.render('admin/index.html')


admin = Admin(app=app, name='Quản lý', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(UserView(User, db.session, name="Người dùng"))
