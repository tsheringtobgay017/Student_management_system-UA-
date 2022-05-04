from flask import request
# from flask_login import current_user
from datetime import datetime
from config import Config
from sqlalchemy import create_engine
from app.admin.util import hash_pass
from uuid import uuid4


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()


def save_user_table():
    id = uuid4()
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    saved = connection.execute(
        'INSERT INTO public."User" ("id", "username", "email", "password") VALUES (%s, %s, %s, %s) RETURNING id',
        (id, username, email, hash_pass(password)))
    user_id = saved.fetchone()
    return user_id['id']


def save_user_detail_table(user_id):
    id = uuid4()
    role = request.form['role']
    ip = request.remote_addr
    browser = request.headers.get('User-Agent')
    connection.execute('INSERT INTO public.user_detail ("id", "user_id", "role", "ip_address", "browser", "created_at") VALUES (%s, %s, %s, %s, %s, %s)',
                       (id, user_id, role, ip, browser, datetime.now()))
    return "saved"


def all_users():
    draw = request.form.get('draw')
    row = request.form.get('start')
    row_per_page = request.form.get('length')
    search_value = request.form['search[value]']
    search_query = ' '
    if (search_value != ''):
        search_query = "AND (U.username LIKE '%%" + search_value + "%%' " \
            "OR U.email LIKE '%%" + search_value + \
            "%%' OR UD.role LIKE '%% "+search_value+"%%') "

    str_query = 'SELECT *, count(*) OVER() AS count_all, U.id as user_id FROM public."User" AS U, public.user_detail as UD WHERE U.type IS NULL '\
                '' + search_query + '' \
                "AND U.id = UD.user_id LIMIT " + row_per_page + " OFFSET " + row + ""

    users = connection.execute(str_query).fetchall()
   

    data = []
    count = 0
    for index, user in enumerate(users):
        data.append({'sl': index + 1,
                     'username': user.username,
                     'email': user.email,
                     'role': user.role,
                     'id': user.user_id})
        count = user.count_all

    respose = {
        "draw": int(draw),
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": data
    }

    return respose


# defining user roles
def user_role():
    con = engine.connect()
    user = con.execute(
        'SELECT UD.role FROM public."User" AS U, public.user_detail as UD WHERE U.id = UD.user_id AND U.username = %s LIMIT 1',
        str('admin')).fetchone()
    return user['role']


def is_admin():
    if(user_role() == 'admin'):
        return True
    else:
        return False


def is_normal():
    if(user_role() == 'normal'):
        return True
    else:
        return False
