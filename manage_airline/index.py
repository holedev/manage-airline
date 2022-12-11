from manage_airline import app, login, controllers

app.add_url_rule('/', 'index', controllers.index, methods=['get', 'post'])

app.add_url_rule('/login', 'login', controllers.login, methods=['get', 'post'])
app.add_url_rule('/oauth', 'login_oauth', controllers.login_oauth)
app.add_url_rule('/callback', 'oauth_callback', controllers.oauth_callback)
app.add_url_rule('/register', 'register', controllers.register, methods=['get', 'post'])
app.add_url_rule('/logout', 'logout', controllers.logout)

app.add_url_rule('/flight_list', 'flight_list', controllers.flight_list, methods=['get'])
app.add_url_rule('/form_ticket/<int:f_id>', 'form_ticket', controllers.form_ticket, methods=['get'])
app.add_url_rule('/pay/<int:f_id>', 'pay', controllers.pay, methods=['get'])
app.add_url_rule('/preview_ticket/<int:u_id>', 'preview_ticket', controllers.preview_ticket, methods=['get'])

app.add_url_rule('/api/flight_schedule', 'create_flight_schedule', controllers.create_flight_schedule, methods=['post'])
app.add_url_rule('/api/flight_schedule/search', 'search_flight_schedule', controllers.search_flight_schedule,
                 methods=['post'])
app.add_url_rule('/api/form_ticket/<int:f_id>', 'create_form_ticket', controllers.create_form_ticket,
                 methods=['post'])
app.add_url_rule('/api/pay/<int:f_id>', 'pay_ticket', controllers.pay_ticket,
                 methods=['post'])
app.add_url_rule('/api/flight_schedule/add/<int:f_id>', 'add_flight_schedule', controllers.add_flight_schedule,
                 methods=['post'])
app.add_url_rule('/api/flight_schedule/delete/<int:f_id>', 'delete_flight_schedule', controllers.delete_flight_schedule,
                 methods=['post'])


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
