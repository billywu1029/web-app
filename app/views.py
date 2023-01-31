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
    return render_template('base.html', title="Home Page")

@views.route('/upload')
def upload():
    return render_template('upload.html', title="Upload Data JSON")

def insert_rows_db(data: dict):
    for row in data:
        row['billable_amount'] = row['actual_amount'] + row['adjustments']
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

        db.drop_all()
        db.create_all()
        insert_rows_db(data)

        return 'File uploaded successfully!'

    return 'Error! file not uploaded successfully'

@views.route('/lineitems/<int:page_num>')
def lineitems(page_num):
    inspector = inspect(db.engine)
    if inspector.has_table(LineItem.__tablename__):
        lineitems = LineItem.query.paginate(per_page=10, page=page_num, error_out=True)
        return render_template('lineitems.html', lineitems=lineitems, title="Display Line Items")
    else:
        return "Error: No DB Table Present. Please upload the data JSON!"

@views.route('/invoice', defaults={'campaign_id': None})
@views.route('/invoice/<string:campaign_id>')
def invoice(campaign_id):
    if not campaign_id:
        sql = f"SELECT SUM(billable_amount) FROM {LineItem.__tablename__}"
    else:
        # TODO get max campaign ID and return an error if inputted id is > than max
        sql = f"SELECT SUM(billable_amount) FROM {LineItem.__tablename__} WHERE campaign_id = {campaign_id}"
    result = db.session.execute(sql).fetchall()
    assert result and result[0]
    invoice = result[0][0]
    return render_template('invoice.html', invoice=invoice, title="Display Invoice")
