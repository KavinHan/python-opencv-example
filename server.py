# coding=utf-8

import os
import urllib.request
from flask import Flask, flash, request, redirect, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
import uuid
from cv_code import blur_image
from db_code import Database

# set host address, allow all ip address
HOST = '0.0.0.0'

# uploaded file extension allowed filtering set
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
# uploaded file saving path
# uploads/src: original image
# uploads/dst: after image processing image
UPLOAD_FOLDER = '/uploads'

# flask setting
app = Flask(__name__, template_folder='template')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# maximum file size
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# static directory path
static_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static')
uploads_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads')

# init database
mysql_db = Database({
            'db_host': '127.0.0.1',
            'db_user': 'root',
            'db_password': 'dongdong',
            'db_port': 3306,
            'db_name': 'mysql-example'
        })


# route: API/
@app.route('/', methods=['GET'])
def serve_dir_directory_index():
    return send_from_directory(static_file_dir, 'index.html')


# route: API/*
@app.route('/<path:path>', methods=['GET'])
def serve_file_in_dir(path):
    if not os.path.isfile(os.path.join(static_file_dir, path)):
        path = os.path.join(path, 'index.html')

    return send_from_directory(static_file_dir, path)


# route: API/uploads/*
@app.route('/uploads/<path:path>', methods=['GET'])
def serve_file_in_upload(path):
    return send_from_directory(uploads_file_dir, path)


# filtering file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# get file extension
def get_extension(filename):
    return filename.rsplit('.', 1)[1].lower()


# save image url to database
def save_image_url(original_url, result_url):
    sql = "INSERT INTO `image` (`original_url`, `result_url`) VALUES ('{!s}', '{!s}')".format(original_url, result_url)
    mysql_db.run_query(sql)


# route: API/api/upload
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print(request.host.split(':')[0])
        request_ip = request.host.split(':')[0]
        # check if the post request has the file part
        if 'file' not in request.files:
            dst = {
                'msg': 'no files',
                'code': 10040
            }
            return jsonify(dst)
        # get file param
        file = request.files['file']
        # generate uuid string for saving filename
        uuid_str = str(uuid.uuid4())
        # create full filename with file extension
        filename = uuid_str + '.' + str(get_extension(file.filename))
        # check the file extension is allow or deny
        if file and allowed_file(file.filename):

            original_url = app.config['UPLOAD_FOLDER'] + '/src/' + filename
            result_url = app.config['UPLOAD_FOLDER'] + '/dst/' + filename
            # save original file to uploads/src folder
            file.save(os.path.join('.' + original_url))
            # save image urls to database
            save_image_url(original_url, result_url)

            # blur the image file by opencv code
            # will saving to uploads/dst folder
            blur_image(filename)

            # return result image file url
            dst = {
                'msg': 'upload file success',
                'code': 200,
                'result_url': 'http://'+request_ip+':5000/uploads/dst/' + filename
            }
            return jsonify(dst)
        else:
            # return error message
            dst = {
                'msg': 'file type not allowed',
                'code': 10050
            }
            return jsonify(dst)


if __name__ == "__main__":
    # run for any ip address
    app.run(host=HOST, port=5000)
