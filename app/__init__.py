from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module


db = SQLAlchemy()


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    for module_name in ('home', 'admin',):
        module = import_module('app.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):
    @app.before_first_request
    def initialize_database():
        db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()


def create_app():
    app = Flask(__name__, static_folder='home/static')
    register_blueprints(app)
    register_extensions(app)
    configure_database(app)
   

    return app
