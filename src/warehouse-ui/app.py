import os
import tempfile
import uuid
import requests
from flask import Flask, flash, redirect, render_template, request
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'files'
app.secret_key = os.urandom(24)

ALLOWED_EXTENSIONS = set(['json'])
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET'])
def fetchData():
    response = requests.request("GET", "http://warehouse/product_all")
    products = response.json()
    # for p in products:
    #     items = ""
    #     for i, art in enumerate(p['inventory']):
    #         items += str(art['name']) + ": " + str(art['amount_of']) + ", "
    #     p['item'] = items

    response = requests.request("GET", "http://warehouse/inventory_all")
    inventory = response.json()

    return render_template('template.html', title='Bootstrap Table', products=products, inventory=inventory)

@app.route('/product_sell/<name>')
def product_sell(name):
    response = requests.request("GET", "http://warehouse/product_sell/" + name)
    response = response.json()
    return response;

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    fileName = 'file1' if 'file1' in request.files else 'file2'
    file = request.files[fileName]
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        path = os.path.join(get_temp_dir(), "file")
        file.save(path)
        file = open(path,'rb')
        if 'file1' == fileName:
            product_upload(file)
        else:
            inventory_upload(file)
        return redirect(request.url.replace("/uploader", ""))
    else:
        flash('File type not supported!')
        return redirect(request.url)

def get_temp_dir():
    tempFolderName = uuid.uuid4().hex
    tempDir = tempfile.gettempdir()
    tempFolderPath = os.path.join(tempDir, tempFolderName)
    tempDir = os.path.join(tempFolderPath)
    if not os.path.exists(tempDir):
        os.mkdir(tempDir)
    return tempDir

def product_upload(file):
    response = requests.post("http://warehouse/product_upload", files = {"file": file})
    response = response.json()
    print(response)
    return response

def inventory_upload(file):
    response = requests.post("http://warehouse/inventory_upload", files = {"file": file})
    response = response.json()
    print(response)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
