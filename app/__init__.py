from flask import Flask, session, g
from flask_login import LoginManager
import flask_login
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
from flask_migrate import Migrate
from datetime import timedelta
from flask_mail import Mail
from numpy.testing._private.utils import jiffies
from sqlalchemy.sql.ddl import DropIndex
from sqlalchemy.sql.schema import ThreadLocalMetaData
from werkzeug import datastructures
from werkzeug.utils import redirect


db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
migrate = Migrate()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app)
    mail.init_app(app)


def register_blueprints(app):
    for module_name in ('home', 'admin', 'class_teacher', 'subject_teacher', 'HR', ):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_session(app):
    @app.before_request
    def make_session_permanent():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=60)
        session.modified = True
        g.user = flask_login.current_user


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app(config):
    app = Flask(__name__, static_folder='home/static')
    app.config.from_object(config)
    register_blueprints(app)
    register_extensions(app)
    configure_database(app)
    configure_session(app)
   
    return app
