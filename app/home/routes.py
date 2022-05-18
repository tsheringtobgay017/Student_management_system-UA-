from flask import render_template, request, jsonify, session, redirect, url_for
from app.home import blueprint
from sqlalchemy import create_engine
from app import db, login_manager
from flask_login import (current_user, login_user, logout_user)
from config import Config
from app.admin.models import User
from app.admin.forms import LoginForm
from app.home.service import store_student_details, store_academic_details, get_dzo_list, get_gewog, get_village,track_std
from flask_login import (current_user, login_required)
from app.admin.util import get_user_by_id, verify_pass, check_user_login_info, update_login_info

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()


@blueprint.route('/')
def route_default():
    return render_template('index.html')


# Route for enroll_student.html and dzongkhang list
@blueprint.route('/enroll-student-detail')
def enroll_page():
    return get_dzo_list()


# Route to store student detail
@blueprint.route('/store-student-info', methods=['POST'])
def store_studentInfo_page():
    id_personal = store_student_details()
    store_academic_details(id_personal)
    return "success"


# Route to fetch gewog list
@blueprint.route("/get-gewog-list", methods=["GET", "POST"])
def get_gewog_list():
    return get_gewog()


# Route to fetch village list
@blueprint.route("/get-village-list", methods=["GET", "POST"])
def get_village_list():
    return get_village()


@blueprint.route('/login', methods=['POST'])
def do_login():
    # read form data
    username = request.form['username']
    password = request.form['password']

    # Locate user
    user = User.query.filter_by(username=username).first()

    s_password = bytearray(user.password)
    # if ip and browser match direct login with otp
    if user:
        if check_user_login_info(user.id):
            # direct login
            if user and verify_pass(password, s_password):
                update_login_info(user.id)
                login_user(user)
                return jsonify({"output": {"fa_required": False, "email": ""}})
                
            return jsonify({"output": {"fa_required": "invalid", "message": "Invalid username or password"}})

        else:
            if user and verify_pass(password, s_password):
                u_data = get_user_by_id(user.id)
                session['l_username'] = username
                session['l_secret'] = password

                return jsonify({"output": {"fa_required": True,  "username": username, "role": u_data.role}})
            else:
                return jsonify({"output": {"fa_required": "invalid", "message": "Invalid username or password"}})
    else:
        return jsonify({"output": {"fa_required": "invalid", "message": "Invalid username or password"}})


# Login & Registration
@blueprint.route('/login-user', methods=['GET'])
def login():
    login_form = LoginForm(request.form)
    if not current_user.is_authenticated:
        return render_template('signin.html',
                               form=login_form)

    else:
         return render_template('signin.html',
                               form=login_form)


# Logout user
@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_blueprint.login'))


# Errors handling
@login_manager.unauthorized_handler
def unauthorized_handler():
    login_form = LoginForm(request.form)
    if not current_user.is_authenticated:
        return render_template('signin.html',
                               form=login_form)
    # return render_template('accounts/login.html'), 403


@blueprint.errorhandler(403)
def access_forbidden(error):
    login_form = LoginForm(request.form)
    if not current_user.is_authenticated:
        return render_template('signin.html',
                               form=login_form)
    # return render_template('accounts/login.html'), 403

# students fee structure
@blueprint.route('/fees-detail')
def studentFee():
    return render_template("std_fee.html")

# track student
@blueprint.route('/track-student')
def trackapplication():
    return render_template("track_std.html")

# track students

@blueprint.route('/search', methods=["POST"])
def search():
    return track_std()
