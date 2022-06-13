from operator import add
from flask import request, render_template
from config import Config
from sqlalchemy import create_engine
from datetime import datetime


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
                     'grade': user.grade,
                     'section': user.section,
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


def update_tbl_std_evaluation():
    student_id = request.form.get('std_id')
    punctuality = request.form.get('punctuality')
    discipline = request.form.get('discipline')
    social_service = request.form.get('socialservice')
    leadership_quality = request.form.get('leadership')
    supw_grade = request.form.get('supw_grade')
    status_remarks = request.form.get('class_status')
    updated_at = datetime.now()
    connection.execute('UPDATE  public.tbl_student_evaluation SET punctuality=%s, discipline=%s, social_service=%s, leadership_quality=%s, supw_grade=%s, status_remarks=%s, updated_at=%s WHERE student_id=%s',
                        punctuality, discipline, social_service, leadership_quality,supw_grade, status_remarks, updated_at, student_id)

    return "ok"


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
        # 'inner join public.tbl_student_evaluation as se on P.id = se. student_id '
        'WHERE P.id =%s',
        id).first()
    return render_template('/pages/add-student/student_detail.html', std=std_class)


# fetching student marks given by subject teacher
def get_std_marks():
    draw = request.form.get('draw')
    row = request.form.get('start')
    row_per_page = request.form.get('length')
    search_value = request.form['search[value]']
    user_id = request.form.get('user_id')
    search_query = ' '
    if (search_value != ''):
        search_query = "AND (A.subject LIKE '%%" + search_value + "%%' "

    str_query = 'SELECT *, count(*) OVER() AS count_all, se.id from public.tbl_student_evaluation as se, public.tbl_students_personal_info as sp, public."User" as U ,public.tbl_academic_detail as ad, '\
                'public.user_detail as ud where se.id IS NOT NULL '\
                '' + search_query + '' \
                "AND sp.id = se.student_id AND U.id = se.subject_teacher_id AND sp.id = ad.std_personal_info_id AND U.id = ud.user_id  LIMIT " + \
        row_per_page + " OFFSET " + row + ""

    get_std_marks = connection.execute(str_query, user_id).fetchall()

    data = []
    count = 0
    for index, user in enumerate(get_std_marks):
        data.append({'sl': index + 1,
                     'subject': user.subject,
                     'class_test_one': user.class_test_one,
                     'mid_term': user.mid_term,
                     'class_test_two': user.class_test_two,
                     'annual_exam': user.annual_exam,
                     'cont_assessment': user.cont_assessment,
                     'total': int(user.class_test_one) + int(user.mid_term) + int(user.class_test_two) + int(user.annual_exam) + int(user.cont_assessment),
                     'id': user.id})
        count = user.count_all

    respose_get_marks = {
        "draw": int(draw),
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": data
    }
    return respose_get_marks


# fetch student details from database
def get_subject_teacher_info(id):
    sub_teacher = connection.execute('SELECT *, se.id FROM public.tbl_student_evaluation AS se '
                                     'INNER JOIN public."User" AS u ON u.id = se.subject_teacher_id '
                                     'INNER JOIN public.user_detail AS ud ON u.id = ud.user_id '
                                     'INNER JOIN public.tbl_students_personal_info AS sp ON sp.id = se.student_id '
                                     'INNER JOIN public.tbl_academic_detail AS ad ON sp.id = ad.std_personal_info_id '
                                     'WHERE se.id =%s',
                                     id).first()
    return render_template('/pages/add-student/view_std_mark.html', sub_teacher=sub_teacher)
