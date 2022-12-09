from flask import redirect, url_for
from manage_airline import app, db, dao
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from manage_airline.models import UserRole, User, FlightSchedule, Airport, BetweenAirport


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class UserView(AuthenticatedModelView):
    column_searchable_list = ['username', 'user_role']
    form_excluded_columns = ['password']
    column_list = ('username', 'fullname')
    column_labels = dict(username='Tên đăng nhập', fullname='Họ tên', image="Ảnh đại diện", user_role="Vai trò")


class AirportView(AuthenticatedModelView):
    column_searchable_list = ['name']
    column_labels = dict(name='Tên sân bay')


class FlightScheView(AuthenticatedModelView):
    @expose('/')
    def index(self):
        airport_list = dao.get_airport_list()
        flight_sche_list = dao.get_flight_sche_list()
        return self.render('admin/flightSche.html', airport_list=airport_list, flight_sche_list=flight_sche_list)


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
admin.add_view(AirportView(Airport, db.session, name='Sân bay'))
admin.add_view(FlightScheView(FlightSchedule, db.session, name='Lịch chuyến bay'))
admin.add_view(AuthenticatedModelView(BetweenAirport, db.session, name='Trung gian'))
