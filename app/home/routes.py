from flask import render_template, request, jsonify, session, redirect, url_for
from app.home import blueprint
from sqlalchemy import create_engine
from config import Config
from app.admin.models import User
from app.admin.forms import LoginForm
from app.home.service import store_student_details, store_academic_details, get_dzo_list, get_gewog, get_village
from flask_login import (current_user, login_required)
from app.admin.util import get_user_by_id, verify_pass

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
    user = 'SELECT * FROM public."User" WHERE username=%s'
    user_list = connection.execute(user, username).first()
    
    s_password = bytearray(user_list.password)
    # if ip and browser match direct login with otp
    if user_list:
        if user_list and verify_pass(password, s_password):
            u_data = get_user_by_id(user_list.id)
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

    return redirect(url_for('admin_blueprint.admin_dashboard'))
