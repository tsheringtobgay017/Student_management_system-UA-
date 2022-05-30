from flask import request, render_template
from config import Config
from sqlalchemy import create_engine
from datetime import datetime
from uuid import uuid4


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()


# fetching student list in class
def get_std_subject_teacher():
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

    get_std = connection.execute(str_query, user_id).fetchall()
    

    data = []
    count = 0
    for index, user in enumerate(get_std):
        data.append({'sl': index + 1,
                     'index_number': user.index_number,
                     'student_cid': user.student_cid,
                     'first_name': user.first_name,
                     'student_email': user.student_email,
                     'id': user.id})
        count = user.count_all

    respose_get_std = {
        "draw": int(draw),
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": data
    }
    return respose_get_std


# fetch student details from database
def get_std_subject_class(id):

    std_class = connection.execute(
        'SELECT *, P.id FROM public.tbl_students_personal_info AS P '
        'inner join public.tbl_academic_detail as A on P.id = A.std_personal_info_id '
        'inner join public.tbl_dzongkhag_list as dzo on dzo.dzo_id = P.student_present_dzongkhag '
        'inner join public.tbl_gewog_list as gewog on gewog.gewog_id = P.student_present_gewog '
        'inner join public.tbl_village_list as village on village.village_id = P.student_present_village '
        'inner join public.tbl_student_evaluation as SE on SE.student_id = P.id '
        'WHERE P.id =%s',
        id).first()
    return render_template('/pages/view-student-table/std_detail.html', std=std_class)



# This is the route for storing student detials into tbl_student_personal_info 
def store_student_assessment_details():
    id = uuid4()
    subject_teacher_id = request.form.get("sub_id")
    student_id = request.form.get("std_id")
    class_test_one = request.form.get("class_test_1")
    class_test_two = request.form.get("class_test_2")
    mid_term = request.form.get("mid_term")
    annual_exam = request.form.get("annual_exam")
    cont_assessment = request.form.get('CA')
    status = request.form.get('std_status')
    punctuality = request.form.get('punctuality')
    discipline = request.form.get("discipline")
    social_service = request.form.get("socialservice")
    leadership_quality = request.form.get("leadership")
    created_at = datetime.now()
    updated_at = datetime.now()

    
    engine.execute("INSERT INTO public.tbl_student_evaluation (id, subject_teacher_id, student_id, class_test_one,  class_test_two, mid_term, annual_exam, cont_assessment,"
                    "status, punctuality, discipline, social_service, leadership_quality, created_at, updated_at) "
                   "VALUES ("
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s)",
                   (id, subject_teacher_id, student_id, class_test_one, class_test_two, mid_term, annual_exam, cont_assessment,status, punctuality, discipline, 
                   social_service,leadership_quality,created_at,  updated_at  ))

    return "successfully"


#checking for cid already exist in database
def check_exist(id):
    check_exist_data = 'SELECT COUNT(*) FROM public.tbl_student_evaluation WHERE student_id =%s'
    results = connection.execute(
        check_exist_data, id).fetchone()[0]
    output = int(results)
    print
    if output > 0:
        return True
    else:
        return False


# fetching student marks given by class teacher
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



