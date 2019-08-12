# coding=utf-8

import os
import urllib.request
from flask import Flask, flash, request, redirect, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
import uuid
from cv_code import blur_image

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = './uploads'

app = Flask(__name__, template_folder='template')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# static directory path
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
uploads_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads')


@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(static_file_dir, 'index.html')


@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)


@app.route('/uploads/<path:path>', methods=['GET'])
def serve_file_in_upload(path):
    return send_from_directory(uploads_file_dir, path)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


@app.route('/api/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            dst = {
                'msg': 'no files',
                'code': 10040
            }
            return jsonify(dst)
        file = request.files['file']
        uuid_str = str(uuid.uuid4())
        filename = uuid_str + '.' + str(get_extension(file.filename))
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/src', filename))
            blur_image(filename)
            dst = {
                'msg': 'upload file success',
                'code': 200,
                'result_url': 'http://127.0.0.1:5000/uploads/dst/' + filename
            }
            return jsonify(dst)
        else:
            dst = {
                'msg': 'file type not allowed',
                'code': 10050
            }
            return jsonify(dst)


if __name__ == "__main__":
    app.run()