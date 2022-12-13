import os
import base64
from flask import jsonify, request, render_template, url_for, redirect, session
from sqlalchemy import create_engine
from config import Config
from datetime import datetime
from uuid import uuid4
from random import randint
from decouple import config
import io

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()
random_id = randint(000, 999)

# This is the route for storing student detials into tbl_student_personal_info 
def store_student_details():
    id = uuid4()
    student_cid = request.form.get("cid")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    dob = request.form.get("dob")
    student_email = request.form.get("email")
    student_phone_number = request.form.get("phone_number")
    student_dzongkhag = request.form.get("permanent_dzongkhag")
    student_gewog = request.form.get("permanent_gewog")
    student_village = request.form.get("permanent_village")
    created_at = datetime.now()
    parent_cid = request.form.get('parent_cid')
    parent_full_name    = request.form.get('parent_name')
    parent_contact_number = request.form.get('parent_number')
    parent_email = request.form.get("parent_email")
    student_present_dzongkhag = request.form.get("present_dzongkhag")
    student_present_gewog = request.form.get("present_gewog")
    student_present_village = request.form.get("present_village")
    status = 'submitted'
    gender = request.form.get('gender')
     # marksheet passport size photo
    half_photo = request.files.get('half_photo', '')

    img_url = os.path.join('./app/home/static/uploads/halfphoto/',
                         student_cid +str(random_id) + half_photo.filename)
    half_photo.save(img_url)
    halfphoto_url = '/static/uploads/halfphoto/'+ student_cid + \
            str(random_id) + half_photo.filename
    


    engine.execute("INSERT INTO public.tbl_students_personal_info (id, student_cid, first_name, last_name, dob, student_email, student_phone_number,  student_dzongkhag, student_gewog, student_village, parent_cid,"
                    "parent_full_name, parent_contact_number, parent_email, student_present_dzongkhag, student_present_gewog, student_present_village, created_at, status,gender, half_photo) "
                   "VALUES ("
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s, %s)",
                   (id, student_cid, first_name, last_name,dob, student_email, student_phone_number, student_dzongkhag, student_gewog, student_village, parent_cid, parent_full_name, parent_contact_number, 
                   parent_email,student_present_dzongkhag,  student_present_gewog, student_present_village,  created_at, status, gender, halfphoto_url))

    return id

# This is the route for storing student detials into tbl_academic_detail 
def store_academic_details(id_personal):
    id = uuid4()
    index_number = request.form.get("index_number")
    previous_school_name = request.form.get("previous_school")
    stream = request.form.get("stream")
     # marksheet upload
    marksheet = request.files.get('marksheet', '')

    img_url = os.path.join('./app/home/static/uploads/marksheet/',
                         index_number +str(random_id) + marksheet.filename)
    marksheet.save(img_url)
    marksheet_url = '/static/uploads/marksheet/'+ index_number + \
            str(random_id) + marksheet.filename
    supw_grade = request.form.get("supw") 
    percentage_obtained = request.form.get("percent")
    created_at = datetime.now()
    admission_for_class = request.form.get('admission_for')
    accommodation = request.form.get('accommodation')
    student_code = request.form.get ('std_code')
    bcse_x = request.form.get ('previous_school_X')
    bhsec_xii = request.form.get('previous_school_XII')
    

    engine.execute("INSERT INTO public.tbl_academic_detail (id, std_personal_info_id, index_number, previous_school_name, stream, marksheet, supw_grade, percentage_obtained,"
                    "created_at, admission_for_class, accommodation, student_code, bcse_x, bhsec_xii) "
                   "VALUES ("
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s,%s)",
                   (id, id_personal, index_number, previous_school_name, stream, marksheet_url, supw_grade, percentage_obtained,  created_at,
                    admission_for_class, accommodation, student_code, bcse_x,bhsec_xii))

    return "success"


# storing contact details
def store_contact_details():
    id = uuid4()
    full_name = request.form.get("Username")
    user_email = request.form.get("Useremail")
    phone_no = request.form.get("phone_number")
    comment = request.form.get("comment")
    created_date = datetime.now()
    updated_date = datetime.now()

    engine.execute("INSERT INTO public.tbl_contact_form (id, full_name, user_email, phone_no, comment, created_date, updated_date) "
                   "VALUES ("
                   "%s,%s,%s,%s,%s,%s,%s)",
                   (id, full_name, user_email, phone_no, comment, created_date, updated_date))

    return 'successful'


# Fetching Dzongkhag/gewog/village list from the database
def get_dzo_list():
    dzongkhag = 'SELECT * FROM public.tbl_dzongkhag_list'
    dzo_List = connection.execute(dzongkhag).fetchall()

    get_user_info = 'select * from public.tbl_dzongkhag_list as dl ' \
                    'inner join public.tbl_gewog_list as gl on dl.dzo_id = gl.dzo_id ' \
                    'inner join public.tbl_village_list as vl on gl.gewog_id = vl.gewog_id'
    get_details = connection.execute(get_user_info).fetchall()
  
    return render_template('enroll_student.html', dzo_List=dzo_List, get_details=get_details)

# Fetching gewog list from database
def get_gewog():
    if request.method == 'POST':
        gewog_id = request.form['gewog_id']
        gewog_list = 'select * from public.tbl_gewog_list where "dzo_id" = %s ORDER BY "gewog_name" ASC'
        gewog_list = connection.execute(gewog_list, gewog_id).fetchall()
    return jsonify({"gewogList": [dict(row) for row in gewog_list]})


# # Fetching village list from the database
def get_village():
    if request.method == 'POST':
        village_id = request.form['village_id']
        village_list = 'SELECT * FROM public.tbl_village_list WHERE "gewog_id" = %s ORDER BY "village_name" ASC'
        village_list = connection.execute(village_list, village_id).fetchall()
    return jsonify({"villageList": [dict(row) for row in village_list]})



def track_std():
   
    student_cid = request.form.get('std_cid')
    index_number = request.form.get('std_index')
    str_query = 'SELECT * FROM public.tbl_students_personal_info as sp inner join public.tbl_academic_detail as ac ON ac.std_personal_info_id = sp.id  WHERE student_cid =%s AND index_number =%s'
    std_list = connection.execute(str_query, student_cid, index_number).fetchall()
    

    data = []
    count = 0
    for index, user in enumerate(std_list):
        data.append({'sl': index + 1,
                     'index_number': user.index_number,
                     'student_cid': user.student_cid,
                     'first_name': user.first_name,
                     'last_name': user.last_name,
                     'student_email': user.student_email,
                     'id': user.id})
      

    respose_std_list = {
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": data
    }
    return respose_std_list


#checking for cid already exist in database
def check_exist(identification_number):
    check_exist_data = 'SELECT COUNT(*) FROM public.tbl_students_personal_info as sp inner join public.tbl_academic_detail as ac ON ac.std_personal_info_id = sp.id  WHERE student_cid =%s'
    results = connection.execute(
        check_exist_data, identification_number).fetchone()[0]
    output = int(results)
    print
    if output > 0:
        return True
    else:
        return False




# printing student result
def printing_result():
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

# paying student fee
def pay_std_fee():
    id = uuid4()
    std_name = request.form.get('std_name')
    std_class = request.form.get('std_class')
    std_section = request.form.get('std_section')
    jrn_number = request.form.get('jrn_number')
    bank_type = request.form.get('bank_type')
    acc_holder = request.form.get('acc_holder')
    connection.execute('INSERT INTO public.tbl_acc_detail("id","std_name", "jrn_number", "bank_type", "acc_holder", "std_class", "std_section") VALUES (%s,%s,%s,%s,%s,%s, %s)',
                       (id, std_name, jrn_number, bank_type, acc_holder, std_class, std_section))

    return "success"

  

