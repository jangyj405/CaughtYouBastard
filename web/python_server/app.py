from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

arr = ["34나 5862", "92로 5796", "88수 8875"]

@app.route('/file', methods=['GET','POST'])
def save_image():
    image = request.files['image']
    print('image is ', image)
    image.save('./save_image/' + secure_filename(image.filename))

    return 'done!'

@app.route('/car-number', methods=['GET', 'POST'])
def find_car_num():

    print("ok")

    resp = make_response(jsonify(arr))
    return resp

@app.route('/car-number/regist', methods=['POST'])
def regist_car_number():
    arr.append({'test': 2})

    return 'done'



if __name__ == '__main__':
    print (app.url_map)
    app.run(host='10.10.14.2', port=4000, debug=True)
