from flask import Blueprint, render_template, request, redirect, url_for, session, flash, g, app
from ..forms import UserLoginForm, UserCreateForm, UserInfo
from ..models import User
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from app import db
import functools
from datetime import timedelta

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None :
        g.user = None
    else :
        g.user = User.query.get(user_id)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view) :
    @functools.wraps(view)
    def wrappend_view(**kwargs) :
        if g.user is None :
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrappend_view


@bp.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@bp.route('/signup/', methods=("GET", "POST"))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            email = User.query.filter_by(email=form.email.data).first()

            if email :
                flash('사용할 수 없는 이메일 주소 입니다.')
            else :
                user = User(username=form.username.data,
                            password=generate_password_hash(form.password1.data),
                            slack_token="not setting",
                            slack_bot="not setting",
                            slack_flag=0,
                            email=form.email.data)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('auth.login'))
        else:
            flash('이미 존재하는 사용자입니다.')

    return render_template('auth/signup.html', form=form)


@bp.route('/login/', methods=("GET", "POST"))
def login():
    form = UserLoginForm()

    if request.method == "POST" and form.validate_on_submit() :
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user :
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data) :
            error = "비밀번호가 올바르지 않습니다."

        if error is None :
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('project._list'))

        flash(error)

    if g.user :
        return redirect(url_for('project._list'))
    else :
        return render_template('auth/login.html', form=form)

@bp.route('/info/', methods=("GET", "POST"))
@login_required
def info():
    userinfo = User.query.get_or_404(g.user.id)
    form = UserInfo()

    if request.method == "POST" :
        error = None
        if form.slack_flag.data == 1 :
            if (form.slack_bot.data == '' or form.slack_bot.data == None) or (form.slack_token.data == '' or form.slack_token.data == None) :
                error = "슬랙 토큰/봇 이름 입력 필요"

        if error == None :
            form.populate_obj(userinfo)
            userinfo.slack_token = form.slack_token.data
            userinfo.slack_bot = form.slack_bot.data
            userinfo.slack_flag = 1 if form.slack_flag.data == 1 else 0

            db.session.commit()

            return render_template('auth/info.html', userinfo=userinfo, form=form)
        else :
            flash(error)
    else :
        form = UserInfo(obj=userinfo)

    return render_template('auth/info.html', userinfo=userinfo, form=form)
