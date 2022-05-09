from flask import request, render_template
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

# for users search


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

# fetch user details


def get_user_by_id(id):
    user = connection.execute(
        'SELECT *, U.id as user_id FROM public."User" AS U, public.user_detail as UD WHERE U.id = UD.user_id AND user_id = %s',
        id).first()
    return user


# delete user details
def delete_user_by_id(id):
    # check self delete
    delete = connection.execute('DELETE FROM public."User" WHERE id=%s', id)
    return True


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


def all_std():
    draw = request.form.get('draw')
    row = request.form.get('start')
    row_per_page = request.form.get('length')
    search_value = request.form['search[value]']
    search_query = ' '
    if (search_value != ''):
        search_query = "AND (A.index_number LIKE '%%" + search_value + "%%' " \
            "OR P.student_cid LIKE '%%" + search_value + \
            "%%' OR P.first_name CONCAT(P.last_name) as full_name LIKE '%% "+search_value+"%%') "

    str_query = 'SELECT *, count(*) OVER() AS count_all, P.id FROM public.tbl_students_personal_info AS P, public.tbl_academic_detail as A WHERE P.id IS NOT NULL  '\
                '' + search_query + '' \
                "AND P.id = A.std_personal_info_id LIMIT " + \
        row_per_page + " OFFSET " + row + ""
    
    users_std = connection.execute(str_query).fetchall()

    data = []
    count = 0
    for index, user in enumerate(users_std):
        data.append({'sl': index + 1,
                     'index_number': user.index_number,
                     'student_cid': user.student_cid,
                     'first_name': user.first_name,
                     'student_email': user.student_email,
                     'id': user.id})
        count = user.count_all

    respose_std = {
        "draw": int(draw),
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": data
    }
    print(":::::::::::", respose_std)
    return respose_std


# fetch student details from database
def get_std_by_id(id):
    std_details = connection.execute(
        'SELECT *, P.id FROM public.tbl_students_personal_info AS P '
        'inner join public.tbl_academic_detail as A on P.id = A.std_personal_info_id '
        'inner join public.tbl_dzongkhag_list as dzo on dzo.dzo_id = P.student_present_dzongkhag '
        'inner join public.tbl_gewog_list as gewog on gewog.gewog_id = P.student_present_gewog '
        'inner join public.tbl_village_list as village on village.village_id = P.student_present_village '
        'WHERE P.id =%s',
        id).first()

    std_info = connection.execute(
        'SELECT *, P.id FROM public.tbl_students_personal_info AS P '
        'inner join public.tbl_academic_detail as A on P.id = A.std_personal_info_id '
        'inner join public.tbl_dzongkhag_list as dzo on dzo.dzo_id = P.student_dzongkhag '
        'inner join public.tbl_gewog_list as gewog on gewog.gewog_id = P.student_gewog '
        'inner join public.tbl_village_list as village on village.village_id = P.student_village '
        'WHERE P.id =%s',
        id).first()
    return render_template('/pages/student-applications/studentinfo.html', std=std_details, std_info=std_info)
