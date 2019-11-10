from flask import Flask, render_template, request
from werkzeug import secure_filename
import base64
import requests


UPLOAD_FOLDER = '/path/to/the/uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
import os, os.path


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLD = '/Users/egurov/projects/hackathon/hack.Genesis/abstract_dog/img_storage/'
UPLOAD_FOLDER = os.path.join(APP_ROOT, UPLOAD_FOLD)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload')
def load_file():
    return render_template('upload.html')

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
        print("\n\n")
        print(svg_img_id)
        get_svg_file(svg_img_id)
        # print("\n\n")
        # print(encoded_string)
        # get_svg_file("040876f071da374ebd99287c6a2e69df")
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
    # response = requests.request("POST", url, data=payload, headers=headers).json()

    print("\n\n")
    print(response["data"])
    print("\n\n")
    print(response["data"]["output"])
    print("\n\n")
    print(response["data"]["output"]["url"])
    # To save to an absolute path.
    r = requests.get(response["data"]["output"]["url"])  
    with open('1.svg', 'wb') as f:
        f.write(r.content)
    # url = "http://api.convertio.co/convert/"+ svg_id +"/status"
    # print("\n\n")
    # print(url)
    # # response = requests.get(url, headers).json()
    # # response = requests.get(url, headers=headers)
    # response = requests.get(url)
    # # response = requests.request("GET", url, data=None, headers=headers).json()
    # print("\n\n")
    # print(response.request.body)

def convert_to_svg(full_jpg_file_path, headers):
    # import base64
    with open(full_jpg_file_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
    # print("\n\n")
    # print(encoded_string)
    # print("\n\n")
    # print(full_jpg_file_path)

    url = "http://api.convertio.co/convert"

    # payload1 = "{\"apikey\" : \"91d6aec6f706564d03d22e730c449e1e\", \"input\" : \"base64\", \"file\" : \""
    # payload2 = "\", \"filename\" : \"test1.jpg\",\"outputformat\":\"svg\"}"
    payload = "{\"apikey\" : \"91d6aec6f706564d03d22e730c449e1e\", \"input\" : \"base64\", \"file\" : \"" + encoded_string.decode("utf-8") + "\", \"filename\" : \"test1.jpg\",\"outputformat\":\"svg\"}"
    # print("\n\n")
    # print(payload)

    response = requests.request("POST", url, data=payload, headers=headers).json()

    # response = {"code":200,"status":"ok","data":{"id":"9ce579e3697b883328dc75312a2e018f","minutes":18}}

    return response["data"]["id"]


# def asdfa():
#     im = Image.open('/Users/egurov/projects/hackathon/hack.Genesis/abstract_dog/img_storage/1.jpg')
#     im.save('Foto.png')
#     bitmap = Bitmap('Foto.png')
#     path = bitmap.trace()

# asdfa()

if __name__ == '__main__':
    app.run(debug = True)
