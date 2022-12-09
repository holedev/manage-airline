from manage_airline import app, login, controllers, dao
from manage_airline.models import UserRole


app.add_url_rule('/', 'index', controllers.index, methods=['get', 'post'])

app.add_url_rule('/login', 'login', controllers.login, methods=['get', 'post'])
app.add_url_rule('/oauth', 'login_oauth', controllers.login_oauth)
app.add_url_rule('/callback', 'oauth_callback', controllers.oauth_callback)
app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout)

app.add_url_rule('/flight_list', 'flight_list', controllers.flight_list, methods=['get'])
app.add_url_rule('/form_ticket', 'form_ticket', controllers.form_ticket, methods=['get'])
app.add_url_rule('/pay', 'pay', controllers.pay, methods=['get'])

app.add_url_rule('/api/flight_schedule', 'create_flight_schedule', controllers.create_flight_schedule, methods=['post'])


@login.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)


@app.context_processor
def common_attributes():
    return {
        'user_role': UserRole
    }


if __name__ == '__main__':
    from manage_airline.admin import *
    app.run(host='localhost', port=5001, debug=True)
