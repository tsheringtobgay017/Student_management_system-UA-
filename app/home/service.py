import os
import numpy as np
import cv2
import base64
from flask import jsonify, request, render_template, url_for, redirect, session
from sqlalchemy import create_engine
from torch import ge
from config import Config
from datetime import datetime
from uuid import uuid4
# from decouple import config
import requests
from requests.structures import CaseInsensitiveDict
import io

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

# This is the route for storing student detials into tbl_student_reg 
def store_student_details():
    id = uuid4()
    student_cid = request.form.get("cid")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
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
    


    engine.execute("INSERT INTO public.tbl_students_personal_info (id, student_cid, first_name, last_name, student_dzongkhag, student_gewog, student_village, parent_cid,"
                    "parent_full_name, parent_contact_number, parent_email, student_present_dzongkhag, student_present_gewog, student_present_village, created_at) "
                   "VALUES ("
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (id, student_cid, first_name, last_name, student_dzongkhag, student_gewog, student_village, parent_cid, parent_full_name, parent_contact_number, parent_email,student_present_dzongkhag,  student_present_gewog, student_present_village,  created_at))

    return "success"


# Fetching Dzongkhag/gewog/village list from the database
def get_dzo_list():
    dzongkhag = 'SELECT * FROM public.tbl_dzongkhag_list'
    dzo_List = connection.execute(dzongkhag).fetchall()
    print(":::::",dzo_List)

    get_user_info = 'select * from public.tbl_dzongkhag_list as dl ' \
                    'inner join public.tbl_gewog_list as gl on dl.dzo_id = gl.dzo_id ' \
                    'inner join public.tbl_village_list as vl on gl.gewog_id = vl.gewog_id'
    get_details = connection.execute(get_user_info).fetchall()
  
    return render_template('enroll_student.html', dzo_List=dzo_List, get_details=get_details)

# Fetching gewog list from database
def get_gewog():
    if request.method == 'POST':
        gewog_id = request.form['gewog_id']
        print(":::",gewog_id)
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