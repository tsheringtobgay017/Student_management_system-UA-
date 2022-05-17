import os
import base64
from flask import jsonify, request, render_template, url_for, redirect, session
from sqlalchemy import create_engine
from config import Config
from datetime import datetime
from uuid import uuid4
from random import randint
# from decouple import config
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
    parent_full_name = request.form.get('parent_name')
    parent_contact_number = request.form.get('parent_number')
    parent_email = request.form.get("parent_email")
    student_present_dzongkhag = request.form.get("present_dzongkhag")
    student_present_gewog = request.form.get("present_gewog")
    student_present_village = request.form.get("present_village")
    status = 'submitted'
    gender = request.form.get('gender')
    


    engine.execute("INSERT INTO public.tbl_students_personal_info (id, student_cid, first_name, last_name, dob, student_email, student_phone_number,  student_dzongkhag, student_gewog, student_village, parent_cid,"
                    "parent_full_name, parent_contact_number, parent_email, student_present_dzongkhag, student_present_gewog, student_present_village, created_at, status,gender) "
                   "VALUES ("
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, %s, %s)",
                   (id, student_cid, first_name, last_name,dob, student_email, student_phone_number, student_dzongkhag, student_gewog, student_village, parent_cid, parent_full_name, parent_contact_number, 
                   parent_email,student_present_dzongkhag,  student_present_gewog, student_present_village,  created_at, status, gender))

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


# def track_std():
#     if request.method == 'POST':
#         student_cid = request.form.get('std_cid')
#         index_number = request.form.get('std_index')
#         get_std = 'SELECT * FROM public.tbl_students_personal_info as sp inner join public.tbl_academic_detail as ac ON ac.std_personal_info_id = sp.id  WHERE student_cid =%s AND index_number =%s'
#         std_list = connection.execute(get_std, student_cid, index_number ).fetchall()
#         print('::::',std_list)
#     return str(std_list)


def track_std():
   
    student_cid = request.form.get('std_cid')
    index_number = request.form.get('std_index')
  
   

    str_query = 'SELECT * FROM public.tbl_students_personal_info as sp inner join public.tbl_academic_detail as ac ON ac.std_personal_info_id = sp.id  WHERE student_cid =%s AND index_number =%s'
       
    

    std_list = connection.execute(str_query, student_cid, index_number).fetchall()
    print(":::::::", std_list)

    data = []
    count = 0
    for index, user in enumerate(std_list):
        data.append({'sl': index + 1,
                     'index_number': user.index_number,
                     'student_cid': user.student_cid,
                     'first_name': user.first_name,
                     'student_email': user.student_email,
                     'id': user.id})
      

    respose_std_list = {
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": data
    }
    return respose_std_list
