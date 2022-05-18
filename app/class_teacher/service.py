from flask import request
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
                "AND U.id = UD.user_id AND UD.role='subject_teacher'  LIMIT " + row_per_page + " OFFSET " + row + ""
    
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
    str_query = 'SELECT * FROM public.tbl_students_personal_info as sp inner join public.tbl_academic_detail as ac ON ac.std_personal_info_id = sp.id  WHERE student_cid =%s AND index_number =%s '
    addstd_list = connection.execute(str_query, student_cid, index_number).fetchall()
    data = []
    count = 0
    for index, user in enumerate(addstd_list):
        data.append({'sl': index + 1,
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
    
    
