from flask import request
from datetime import datetime
from sqlalchemy.sql.functions import user
from config import Config
from sqlalchemy import create_engine
from app.admin.util import hash_pass
from uuid import uuid4


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

def save_user_table():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']

    saved = connection.execute(
        'INSERT INTO public."User" ("username", "email", "password") VALUES (%s, %s, %s) RETURNING id',
        (username, email, hash_pass(password)))
    user_id = saved.fetchone()
    return user_id['id']


def save_user_detail_table(user_id):
        id = uuid4()
        role = request.form['role']
        ip = request.remote_addr
        browser = request.headers.get('User-Agent')
        connection.execute('INSERT INTO public.user_detail ("id", "user_id", "role", "ip_address", "browser", "created_at") VALUES (%s, %s, %s, %s, %s, %s)',
                        (id, user_id, role, ip, browser, datetime.now()))
        return "saved"