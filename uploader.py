from flask import Flask, render_template, request
from werkzeug import secure_filename
import base64
import requests
from config import convertio_co_api_key


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import os, os.path

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/Users/egurov/projects/hackathon/hack.Genesis/abstract_dog/img_storage/'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def load_file():
    return render_template('index.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))

        headers = {
            'Content-Type': "application/json",
            'User-Agent': "PostmanRuntime/7.19.0",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Postman-Token': "d5355c34-e9f2-4788-9902-d65075220528,ed0cd50c-ebb8-4b12-8342-b983d11d7ea3",
            'Host': "api.convertio.co",
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "1324237",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

        svg_img_id = convert_to_svg(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)), headers)
        get_svg_file(svg_img_id)
    return 'file uploaded successfully'

def get_svg_file(svg_id):
    url = "http://api.convertio.co/convert/"+ svg_id +"/status"
    print("\n\n")
    print(url)

    headers = {
        'User-Agent': "PostmanRuntime/7.19.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "e954d0db-1905-459b-b417-215b4f476ea3,34bcf8fc-beaf-495f-b4df-b7fc3d937259",
        'Host': "api.convertio.co",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers).json()
    r = requests.get(response["data"]["output"]["url"])  
    with open('1.svg', 'wb') as f:
        f.write(r.content)

def convert_to_svg(full_jpg_file_path, headers):
    with open(full_jpg_file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    url = "http://api.convertio.co/convert"
    payload = "{\"apikey\" : \"91d6aec6f706564d03d22e730c449e1e\", \"input\" : \"base64\", \"file\" : \"" + encoded_string.decode("utf-8") + "\", \"filename\" : \"test1.jpg\",\"outputformat\":\"svg\"}"

    response = requests.request("POST", url, data=payload, headers=headers).json()
    return response["data"]["id"]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8011, debug = True)
