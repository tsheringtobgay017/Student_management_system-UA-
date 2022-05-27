from operator import add
from flask import request, render_template
from config import Config
from sqlalchemy import create_engine


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()


def subject_teacher():
    draw = request.form.get('draw')
    row = request.form.get('start')
    row_per_page = request.form.get('length')
    search_value = request.form['search[value]']
    search_query = ' '
    if (search_value != ''):
        search_query = "AND (U.username LIKE '%%" + search_value + "%%' " \
            "OR U.email LIKE '%%" + search_value + \
            "%%' OR UD.role LIKE '%% "+search_value+"%%') "

    str_query = 'SELECT *, count(*) OVER() AS count_all, U.id as user_id FROM public."User" AS U, public.user_detail as UD WHERE U.type IS NULL'\
                '' + search_query + '' \
                "AND U.id = UD.user_id AND UD.role='subject_teacher'  LIMIT " + \
        row_per_page + " OFFSET " + row + ""

    subject_teacher = connection.execute(str_query).fetchall()
    data = []
    count = 0
    for index, user in enumerate(subject_teacher):
        data.append({'sl': index + 1,
                     'username': user.username,
                     'email': user.email,
                     'subject': user.subject,
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


def search_std():
    student_cid = request.form.get('cid')
    index_number = request.form.get('index_num')
    str_query = 'SELECT * FROM public.tbl_students_personal_info as sp inner join public.tbl_academic_detail as ac ON ac.std_personal_info_id = sp.id  WHERE student_cid =%s AND index_number =%s  '
    addstd_list = connection.execute(
        str_query, student_cid, index_number).fetchall()
    data = []
    count = 0
    for index, user in enumerate(addstd_list):
        data.append({'sl': index + 1,
                     'id': user.id,
                     'index_number': user.index_number,
                     'student_cid': user.student_cid,
                     'first_name': user.first_name,
                     'last_name': user.last_name,
                     'student_email': user.student_email,
                     'status': user.status,
                     'id': user.id})

    respose_addstd_list = {
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": data,
    }

    return respose_addstd_list


def update_tbl_academic():
    index_number = request.form.get('index_num')
    user_id = request.form.get('user_id')
    connection.execute('UPDATE  public.tbl_academic_detail SET user_id=%s WHERE index_number=%s',
                       user_id, index_number)

    return user_id



# fetching student list in class
def get_std_in_class():
    draw = request.form.get('draw')
    row = request.form.get('start')
    row_per_page = request.form.get('length')
    search_value = request.form['search[value]']
    user_id = request.form.get('user_id')
    search_query = ' '
    if (search_value != ''):
        search_query = "AND (A.index_number LIKE '%%" + search_value + "%%' " \
            "OR P.student_cid LIKE '%%" + search_value + "%%' "\
            "OR P.first_name LIKE '%% " + search_value+"%%') "\
            "OR P.student_email LIKE '%%" + search_value + "%%' "

    str_query = 'SELECT *, count(*) OVER() AS count_all, P.id FROM public.tbl_students_personal_info AS P, public.tbl_academic_detail as A, public."User" as U WHERE P.id IS NOT NULL  '\
                '' + search_query + '' \
                "AND P.id = A.std_personal_info_id AND A.user_id = U.id LIMIT " + \
        row_per_page + " OFFSET " + row + ""

    add_std = connection.execute(str_query, user_id).fetchall()
    

    data = []
    count = 0
    for index, user in enumerate(add_std):
        data.append({'sl': index + 1,
                     'index_number': user.index_number,
                     'student_cid': user.student_cid,
                     'first_name': user.first_name,
                     'student_email': user.student_email,
                     'id': user.id})
        count = user.count_all

    respose_add_std = {
        "draw": int(draw),
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": data
    }
    return respose_add_std


# fetch student details from database
def get_std_class(id):
    std_class = connection.execute(
        'SELECT *, P.id FROM public.tbl_students_personal_info AS P '
        'inner join public.tbl_academic_detail as A on P.id = A.std_personal_info_id '
        'inner join public.tbl_dzongkhag_list as dzo on dzo.dzo_id = P.student_present_dzongkhag '
        'inner join public.tbl_gewog_list as gewog on gewog.gewog_id = P.student_present_gewog '
        'inner join public.tbl_village_list as village on village.village_id = P.student_present_village '
        'WHERE P.id =%s',
        id).first()
    return render_template('/pages/add-student/student_detail.html', std=std_class)