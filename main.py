import os
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
from vision.vision import get_defect

UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./uploaded-images"

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/defect', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return "no file uploaded"
    file = request.files['file']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
        result =  get_defect(save_path)
        response = jsonify(result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

@app.route('/health', methods=['GET'])
def healthy():
    return "i'm healthy, thanks", 200