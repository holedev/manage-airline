from flask import render_template,  request, redirect
from manage_airline import dao
from manage_airline.models import UserRole
from flask_login import login_user, logout_user
from manage_airline.decorators import anonymous_user


def index():
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


def logout():
    logout_user()
    return redirect('/login')
