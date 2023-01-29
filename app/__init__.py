from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
DB_NAME = "database.db"

FILE_MAX_SIZE_BYTES = 500000000
UPLOAD_FOLDER = "uploads/"  # Relative to cwd (project root)


def initialize_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'blah'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_PATH'] = FILE_MAX_SIZE_BYTES

    from .views import views
    from .models import LineItem

    app.register_blueprint(views, url_prefix='/')
    create_database(app)

    return app


def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')
    else:
        print('Database Already Exists!')
