from flask import redirect, url_for, session, flash
from manage_airline import app, db, dao
from flask_admin import Admin, AdminIndexView, expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from manage_airline.models import UserRole, User, FlightSchedule, Airport, BetweenAirport, ADMINRules
import json


class AuthenticatedView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class AuthenticatedAdminView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedAdmin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.ADMIN


class AuthenticatedStaff(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.user_role == UserRole.STAFF


class UserView(AuthenticatedAdmin):
    column_searchable_list = ['username', 'user_role']
    form_excluded_columns = ['password']
    column_list = ('username', 'fullname')
    column_labels = dict(username='Tên đăng nhập', fullname='Họ tên', image="Ảnh đại diện", user_role="Vai trò")


class AirportView(AuthenticatedAdmin):
    column_searchable_list = ['name']
    column_labels = dict(name='Tên sân bay')


class FlightScheView(AuthenticatedStaff):
    @expose('/')
    def index(self):
        airport_list = dao.get_airport_list()
        flight_sche_list = dao.get_flight_sche_list()
        rules = dao.get_admin_rules_latest()
        return self.render('admin/flightSche.html', airport_list=airport_list, flight_sche_list=flight_sche_list,
                           rules=rules)


class RulesView(AuthenticatedAdmin):
    @expose('/')
    def index(self):
        rules = dao.get_admin_rules_latest()
        rules_list = dao.get_admin_rules_list()
        return self.render('admin/rules.html', rules=rules, rules_list=rules_list)


class MyAdminView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated:
            return redirect('/login')
        if current_user.user_role == UserRole.USER:
            return redirect('/')
        f_list = dao.get_flight_sche_list()
        a_list = dao.get_airport_list()
        return self.render('admin/index.html', user_role=UserRole, f_list=f_list, a_list=a_list)


class LogoutView(AuthenticatedView):
    @expose('/')
    def index(self):
        logout_user()
        session.clear()
        return redirect('/login')


class HomeView(AuthenticatedView):
    @expose('/')
    def index(self):
        return redirect('/')


class StatsView(AuthenticatedAdminView):
    @expose('/')
    def index(self):
        data_stats = dao.get_data_stats_json_list()
        return self.render('admin/stats.html', data_stats=data_stats)


admin = Admin(app=app, name='Quản lý', template_mode='bootstrap4', index_view=MyAdminView())
admin.add_view(UserView(User, db.session, name="Người dùng"))
admin.add_view(AirportView(Airport, db.session, name='Sân bay'))
admin.add_view(RulesView(ADMINRules, db.session, name='Quy định'))
admin.add_view(FlightScheView(FlightSchedule, db.session, name='Lịch chuyến bay'))
admin.add_view(StatsView(name="Thống kê báo cáo"))
admin.add_view(HomeView(name='Trang chủ người dùng'))
admin.add_view(LogoutView(name='Đăng xuất'))
