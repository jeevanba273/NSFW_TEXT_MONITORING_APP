import os
import urllib.request
from flask import *
from werkzeug.utils import secure_filename
import filetype
import requests
import json
import cv2
import cloudinary
import cloudinary.uploader as up
import os
cloudinary.config.update = ({
    'cloud_name':'drlf6gntz',
    'api_key': '894749617857176',
    'api_secret': 'Qp-ckIp4k_xIresVZF7Gms0WrPY'
})

url = 'http://localhost:5000/'

upload_folder = r".\static\uploads"

app = Flask(__name__)

app.secret_key = 'dsdsqqwqw'
contents=[]
@app.route('/')
def upload_form():

    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    try:
        if request.is_json:
            data = request.get_json()  # Safely parse the JSON data
            text = data.get("text")
            if text:
                j_data = json.dumps({"data": text, "type": "text"})
                headers = {'Content-Type': 'application/json'}
                response = requests.post(url, data=j_data, headers=headers)
                if response.text.split()[0] == "true":
                    return render_template("index.html", content="Valid response received")
                else:
                    return render_template("index.html", content="Invalid Text")
            else:
                return "No text provided", 400
        else:
            return "Request body must be JSON", 400
    except Exception as e:
        return f"An error occurred: {str(e)}", 500



if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)
