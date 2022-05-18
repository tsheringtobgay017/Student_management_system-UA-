from os import stat
from flask import request, render_template
from flask_login import current_user
from datetime import datetime
from config import Config
from flask_mail import Message
from app import mail
from sqlalchemy import create_engine
from app.admin.util import hash_pass
from uuid import uuid4
import requests
from requests.structures import CaseInsensitiveDict


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
