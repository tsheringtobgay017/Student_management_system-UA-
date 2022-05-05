import binascii
import hashlib
from itertools import count
import os
from flask_mail import Message
from matplotlib.pyplot import connect
from sqlalchemy.sql.functions import current_timestamp, user
from flask import jsonify, request
from config import Config
from sqlalchemy import create_engine, null
import datetime


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()


def hash_pass(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'),
                                  salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash)  # return bytes


def verify_pass(provided_password, stored_password):
    """Verify a stored password against one provided by user"""
    stored_password = stored_password.decode('ascii')
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  provided_password.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password


def update_login_info(user_id):
    ip = request.remote_addr
    browser = request.headers.get('User-Agent')
    connection.execute(
        'UPDATE public.user_detail SET "ip_address" = %s, "browser"=%s, "last_login"=%s WHERE "user_id"=%s',
        (ip, browser, datetime.datetime.now(), user_id))
    return True


def check_user_login_info(user_id):
    ip = request.remote_addr
    browser = request.headers.get('User-Agent')
    check = connection.execute(
        'SELECT * FROM public.user_detail WHERE "user_id"=%s AND "ip_address"=%s',
        (user_id, ip)).fetchall()
    if len(check) > 0:
        return True
    else:
        return False

def get_user_by_id(user_id):
    user = connection.execute(
        'SELECT * FROM public.user_detail WHERE "user_id"=%s',
        (user_id)).fetchone()
    return user
