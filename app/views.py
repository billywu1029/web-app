import os

from flask import Blueprint, render_template, request, flash, jsonify
from werkzeug.utils import secure_filename
from . import UPLOAD_FOLDER
import json

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    fnames = os.listdir(UPLOAD_FOLDER)
    if not any(fname.endswith('.json') for fname in fnames):
        return "<h>No data uploaded yet!</h1>"

    assert len(fnames) == 1
    with open(os.path.join(UPLOAD_FOLDER, fnames[0]), "r") as f:
        data = json.load(f)
        print(data[0])
    return "<h>Yee</h>"

@views.route('/upload')
def upload():
    return render_template('upload.html')

@views.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(UPLOAD_FOLDER, secure_filename(f.filename)))
        return 'file uploaded successfully'
    return 'error! file not uploaded successfully'

