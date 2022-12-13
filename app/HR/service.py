from operator import add
from uuid import uuid4
from flask import request, render_template,jsonify
from config import Config
from sqlalchemy import create_engine
from datetime import datetime
from random import randint
import os


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()
random_id = randint(000, 999)

def get_student_fee():
    draw = request.form.get('draw')
    row = request.form.get('start')
    row_per_page = request.form.get('length')
    search_value = request.form['search[value]']
    id = request.form.get('id')
    search_query = ' '
    if (search_value != ''):
        search_query = "AND (P.std_name LIKE '%%" + search_value + "%%' " \
            "OR P.jrn_number LIKE '%%" + search_value + "%%' "\
            "OR P.acc_holder LIKE '%% " + search_value+"%%') "
    str_query = 'SELECT *, P.id FROM public.tbl_acc_detail AS P WHERE P.id IS NOT NULL '\
                '' + search_query + '' + \
                    "LIMIT " +\
        row_per_page + " OFFSET " + row + ""
    

    add_std_fee = connection.execute(str_query, id).fetchall()
    data = []
    count = 0
    for index, usr in enumerate(add_std_fee):
        data.append({'sl': index + 1,
                    'std_name': usr.std_name,
                    'std_class': usr.std_class,
                    'std_section': usr.std_section,
                    'jrn_number': usr.jrn_number,
                    'acc_holder': usr.acc_holder,
                    'bank_type': usr.bank_type,
                    'id': id})
    respose_add_std = {
        "draw": int(draw),
        "iTotalRecords": count,
        "iTotalDisplayRecords": count,
        "aaData": data
    }
    return respose_add_std
