import os
import json
import boto3
from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import inspect
from werkzeug.utils import secure_filename
from config import S3_BUCKET, S3_KEY, S3_SECRET
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
        file = request.files['file']
        file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
        fnames = os.listdir(UPLOAD_FOLDER)
        if not all(fname.endswith('.json') for fname in fnames):
            for fname in fnames:
                if not fname.endswith('.json'):
                    print(f"Removing {fname}. Not JSON format.")
                    os.remove(os.path.join(UPLOAD_FOLDER, fname))
            return "<h>Uploaded a non-JSON file!</h1>"

        with open(os.path.join(UPLOAD_FOLDER, fnames[0]), "r") as f:
            data = json.load(f)

        db.drop_all()
        db.create_all()
        insert_rows_db(data)
        print('File uploaded successfully to DB!')  # Ideally would want to flash/alert to user or log on server

        # Future iterations: export the database.db itself as a file on Amazon S3
        # (this way it would allow us to reflect any modifications made via the web app)
        try:
            # **Very important to reset the read cursor on the file so that there are bytes to read from** #
            file.seek(0)
            s3_resource = boto3.resource(
                's3',
                aws_access_key_id=S3_KEY,
                aws_secret_access_key=S3_SECRET
            )
            bucket = s3_resource.Bucket(S3_BUCKET)
            bucket.Object(file.filename).put(Body=file)
            print('File exported successfully to Amazon S3!')
        except Exception as e:
            print("Failed to export JSON to Amazon S3!")
            print(e)
            return redirect(url_for('views.upload'))

        return redirect(url_for('views.lineitems', page_num=1))

    print('Error! file not uploaded successfully')
    return redirect(url_for('views.upload'))

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
    inspector = inspect(db.engine)
    if not inspector.has_table(LineItem.__tablename__):
        return "Error: No DB Table Present. Please upload the data JSON!"
    if not campaign_id:
        sql = f"SELECT SUM(billable_amount) FROM {LineItem.__tablename__}"
    else:
        # TODO get max campaign ID and return an error if inputted id is > than max
        sql = f"SELECT SUM(billable_amount) FROM {LineItem.__tablename__} WHERE campaign_id = {campaign_id}"
    result = db.session.execute(sql).fetchall()
    assert result and result[0]
    invoice = result[0][0]
    return render_template('invoice.html', invoice=invoice, title="Display Invoice")
