from flask import request

from sqlalchemy.sql.functions import user
from config import Config
from sqlalchemy import create_engine
from app.admin.util import hash_pass

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