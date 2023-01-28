from flask import Flask

FILE_MAX_SIZE_BYTES = 500000000
UPLOAD_FOLDER = "uploads/"  # Relative to cwd (project root)

def initialize_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'blah'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_PATH'] = FILE_MAX_SIZE_BYTES

    from .views import views
    app.register_blueprint(views, url_prefix='/')

    return app
