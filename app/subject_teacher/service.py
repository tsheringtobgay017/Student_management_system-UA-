from flask import request
from config import Config
from sqlalchemy import create_engine


engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
connection = engine.connect()

