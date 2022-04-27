import os
import numpy as np
import cv2
import base64
from flask import jsonify, request, render_template, url_for, redirect, session
from sqlalchemy import create_engine
from config import Config
from datetime import datetime
from uuid import uuid4
from decouple import config
import requests
from requests.structures import CaseInsensitiveDict
import io

engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

# This is the route for storing student detials into tbl_student_reg 
def store_student_details():
    id = uuid4()
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    address = request.form.get("address")
    created_at = datetime.now()
    city = request.form.get('city')
    state = request.form.get('state')
    zip_code = request.form.get('zip_code')
    title = request.form.get("title")
    company = request.form.get("company")
    phone_number = request.form.get("phone_number")
    email_address = request.form.get("email_address")
    website = request.form.get("website")


    engine.execute("INSERT INTO public.tbl_student_reg (id, first_name, last_name, address, city, state, zip_code, title, company, phone_number, email_address, website,"
                   "created_at) "
                   "VALUES ("
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                   (id, first_name, last_name, address, city, state, zip_code, title, company, phone_number,email_address,  website,  created_at))

    return "success"


# Fetching Dzongkhag/gewog/village list from the database
def get_dzo_list():
    dzongkhag = 'SELECT * FROM public.tbl_dzongkhag_list'
    dzo_List = connection.execute(dzongkhag).fetchall()
    print("::::",dzo_List)

    get_user_info = 'select *, public.tbl_gewog_list as gewog on gewog.gewog_id = trad.present_gewog ' \
                    'inner join public.tbl_village_list as village on village.village_id = trad.present_village ' 
    get_details = connection.execute(get_user_info).fetchone()
    print("::::", get_details)
   
    return render_template('enroll_student.html', dzo_List=dzo_List, info=get_details)


# Fetching gewog list from database
# def get_gewog():
#     if request.method == 'POST':
#         gewog_id = request.form['gewog_id']
#         gewog_list = 'select * from public.tbl_gewog_list where "dzo_id" = %s ORDER BY "gewog_name" ASC'
#         gewog_list = connection.execute(gewog_list, gewog_id).fetchall()
#     return jsonify({"gewogList": [dict(row) for row in gewog_list]})


# # Fetching village list from the database
# def get_village():
#     if request.method == 'POST':
#         village_id = request.form['village_id']
#         village_list = 'SELECT * FROM public.tbl_village_list WHERE "gewog_id" = %s ORDER BY "village_name" ASC'
#         village_list = connection.execute(village_list, village_id).fetchall()
#     return jsonify({"villageList": [dict(row) for row in village_list]})