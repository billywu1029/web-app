import os
from app import initialize_app, UPLOAD_FOLDER

app = initialize_app()

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
