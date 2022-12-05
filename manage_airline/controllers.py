from flask import render_template, redirect, session, request, url_for
from manage_airline import dao, db, flow
from manage_airline.models import UserRole, User
from flask_login import login_user, logout_user, current_user
from manage_airline.decorators import anonymous_user


def index():
    if request.method.__eq__('POST'):
        return redirect("/flight_list")
    return render_template('index.html')


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
            n = request.args.get('next')
            return redirect(n if n else '/')
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
    return redirect("/")


def logout():
    logout_user()
    return redirect('/login')


def flight_list():
    return render_template('flightList.html')
