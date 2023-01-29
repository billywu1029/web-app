import os
import json
from flask import Blueprint, render_template, request
from flask_sqlalchemy import inspect
from werkzeug.utils import secure_filename
from . import UPLOAD_FOLDER, db
from .models import LineItem

views = Blueprint('views', __name__)

@views.route('/', methods=['GET'])
def home():
    if request.method == 'GET':
        inspector = inspect(db.engine)
        if inspector.has_table(LineItem.__tablename__):
            return "Found the db table"
        else:
            return "No db table rip"
    return "<h>Yee</h>"

@views.route('/lineitems/<int:page_num>')
def lineitems(page_num):
    lineitems = LineItem.query.paginate(per_page=10, page=page_num, error_out=True)
    return render_template('lineitems.html', lineitems=lineitems)

@views.route('/upload')
def upload():
    return render_template('upload.html')

def insert_rows_db(data: dict):
    for row in data:
        db.session.add(LineItem(**row))
    db.session.commit()

@views.route('/uploader', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))

        fnames = os.listdir(UPLOAD_FOLDER)
        if not any(fname.endswith('.json') for fname in fnames):
            return "<h>No data uploaded yet!</h1>"

        with open(os.path.join(UPLOAD_FOLDER, fnames[0]), "r") as f:
            data = json.load(f)
            print(data[0])  # TODO: remove

        db.drop_all()
        db.create_all()
        insert_rows_db(data)

        return 'file uploaded successfully'

    return 'error! file not uploaded successfully'
