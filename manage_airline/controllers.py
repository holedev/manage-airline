from flask import render_template, redirect, request, session
from manage_airline import dao, db, flow
from manage_airline.models import UserRole, User
from flask_login import login_user, logout_user, current_user
from manage_airline.decorators import anonymous_user


def index():
    airport_list = dao.get_airport_list()
    return render_template('index.html', airport_list=airport_list)


@anonymous_user
def login():
    if request.method.__eq__('POST'):
        username = request.form['username']
        password = request.form['password']

        user = dao.auth_user(username=username, password=password)

        if user:
            login_user(user=user)
            if user.user_role == UserRole.ADMIN:
                return redirect('/admin')
            return redirect('/')
        else:
            return render_template('login.html', error="Sai tên tài khoản hoặc mật khẩu!")
    return render_template('login.html')


@anonymous_user
def register():
    err_msg = ''
    if request.method == 'POST':
        password = request.form['password']
        confirm = request.form['confirm']
        if password.__eq__(confirm):
            try:
                dao.register(fullname=request.form['fullname'],
                             username=request.form['username'],
                             password=password)

                return redirect('/login')
            except:
                err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            err_msg = 'Mật khẩu không khớp!'

    return render_template('register.html', err_msg=err_msg)


def login_oauth():
    authorization_url, state = flow.authorization_url()
    return redirect(authorization_url)


def oauth_callback():
    user_oauth = dao.get_user_oauth()
    email = user_oauth['email']
    user = User.query.filter_by(username=email).first()
    if user is None:
        import hashlib
        password = str(hashlib.md5('123456'.encode('utf-8')).hexdigest())
        fullname = user_oauth['name']
        image = user_oauth['picture']
        user = User(fullname=fullname, username=email, password=password, image=image)
        db.session.add(user)
        db.session.commit()
    login_user(user)
    if user.user_role == UserRole.ADMIN:
        return redirect('/admin')
    return redirect("/")


def logout():
    logout_user()
    session.clear()
    return redirect('/login')


def flight_list():
    return render_template('flightList.html')


def form_ticket(f_id):
    f = dao.get_flight_sche_json(f_id)
    return render_template('formTicket.html', f=f, user_role=UserRole)


def pay(f_id):
    return render_template('pay.html')


def create_flight_schedule():
    data = request.get_json()
    if request.method == 'POST':
        try:
            f = dao.create_flight_sche(airport_from=data['airport_from'], airport_to=data['airport_to'],
                                       time_start=data['time_start'],
                                       time_end=data['time_end'], quantity_ticket_1st=data['quantity_1st'],
                                       quantity_ticket_2nd=data['quantity_2nd'])
            for ab in data['ab_list']:
                bwa = dao.create_bwa(airport_id=ab['ap_id'], flight_sche_id=f.id, time_stay=ab['ap_stay'],
                                     note=ab['ap_note'])
        except Exception as err:
            return {
                'status': 500,
                'data': err
            }
    if request.method == 'PATCH':
        try:

            f = dao.update_flight_sche(f_id=data['id'], airport_from=data['airport_from'],
                                       airport_to=data['airport_to'],
                                       time_start=data['time_start'],
                                       time_end=data['time_end'], quantity_ticket_1st=data['quantity_1st'],
                                       quantity_ticket_2nd=data['quantity_2nd'])
            f = dao.del_abw_list(f.id)
            for ab in data['ab_list']:
                print(ab)
                bwa = dao.create_bwa(airport_id=ab['ap_id'], flight_sche_id=data['id'], time_stay=ab['ap_stay'],
                                     note=ab['ap_note'])
        except Exception as err:
            return {
                'status': 500,
                'data': err
            }
    return {
        'status': 200,
        'data': 'success'
    }


def search_flight_schedule():
    data = request.get_json()
    inp_search = dao.get_inp_search_json(af_id=data['airport_from'], at_id=data['airport_to'],
                                         time_start=data['time_start'], ticket_type=data['ticket_type'])

    data_search = dao.search_flight_schedule(ap_from=data['airport_from'], ap_to=data['airport_to'],
                                             time_start=data['time_start'], ticket_type=data['ticket_type'])
    session['data_search'] = data_search
    session['inp_search'] = inp_search
    return {
        'status': 200,
        'data': data_search
    }


def create_form_ticket(f_id):
    data = request.get_json()
    session['form_ticket'] = data
    remain_ticket = dao.get_ticket_remain(data['f_id'], int(data['ticket_type']))
    if remain_ticket < data['customers_info'][0]['quantity']:
        return {
            'status': 500,
            'data': "Chỉ có thể đặt tối đa %s vé!" % remain_ticket
        }

    if data['user_role'] == 'UserRole.USER':
        check_time = dao.check_time(data['f_id'])
        if not check_time:
            return {
                'status': 500,
                'data': "Không thể đặt vé cách giờ bay trước 12 tiếng!"
            }
    else:
        check_time = dao.check_time(data['f_id'], is_user=False)
        if not check_time:
            return {
                'status': 500,
                'data': "Không thể đặt vé cách giờ bay trước 4 tiếng!"
            }
        pay_ticket(data['f_id'], is_staff=True)
    return {
        'status': 200,
        'data': data['f_id']
    }


def pay_ticket(f_id, is_staff=False):
    data = request.get_json()
    print(data)
    if not is_staff:
        check_paypal = dao.check_paypal(number_card=data['number_card'], mm_yy=data['mmYY'], cvc_code=data['cvcCode'],
                                        name=data['name'])
    else:
        check_paypal = True
    if check_paypal:
        data_ticket = session.get('form_ticket')
        data_customer = data_ticket['customers_info'][0]['data']
        for c in data_customer:
            package_price = 0
            if c['id'] == 2:
                package_price = data_ticket['package_price']
            c = dao.create_ticket(u_id=current_user.get_id(), f_id=data_ticket['f_id'],
                                  t_type=data_ticket['ticket_type'], t_package_price=package_price, c_name=c['name'],
                                  c_phone=c['phone'], c_id=c['id_customer'])
    return {
        'status': 200,
        'data': 'success'
    }


def preview_ticket(u_id):
    t_list_json = dao.get_ticket_list_json(u_id)
    return render_template("previewTicket.html", t_list_json=t_list_json)


def add_flight_schedule(f_id):
    data = request.get_json()
    f = dao.add_flight_schedule(f_id, data['price'])
    return {
        'status': 200,
        'data': f.id
    }


def delete_flight_schedule(f_id):
    f = dao.delete_flight_schedule(f_id)
    return {
        'status': 200,
        'data': f.id
    }


def confirm_user():
    data = request.get_json()
    u = dao.confirm_user(u_id=current_user.id, password=data['password'])
    if u:
        return {
            'status': 200,
            'data': 'success'
        }
    return {
        'status': 500,
        'data': 'error'
    }


def create_admin_rules():
    data = request.get_json()
    ar = dao.create_admin_rules(min_time_flight_sche=data['min_time_flight_sche'],
                                min_time_stay_airport=data['min_time_stay_airport'],
                                max_time_stay_airport=data['max_time_stay_airport'],
                                max_between_airport_quantity=data['max_between_airport_quantity'],
                                customer_time_ticket=data['customer_time_ticket'],
                                staff_time_ticket=data['staff_time_ticket'])
    if ar is None:
        return {
            'status': 500,
            'data': 'error'
        }
    return {
        'status': 200,
        'data': 'success'
    }
