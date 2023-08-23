from flask import Flask, request, make_response, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import pymysql
import pymysqlpool

pymysqlpool.logger.setLevel('DEBUG')
config = {'host':'localhost', 'user':'root', 'password':'intel123', 'db':'intel_project', 'charset':'utf8'}
pool1 = pymysqlpool.ConnectionPool(size=2, maxsize=3, pre_create_num=2, name='pool1', **config)

con1 = pool1.get_connection()
#conn = pool1.get_connection()

conn = pymysql.connect(host="localhost", user="root", password="intel123", db="intel_project", charset='utf8')

cur = con1.cursor()


app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


@app.route('/file', methods=['GET','POST'])

def save_image():
    image = request.files['image']
    print('image is ', image)
    image.save('./save_image/' + secure_filename(image.filename))

    return 'done!'

@app.route('/car-number-list', methods=['GET'])
def find_car_num_list():
    arr = []
    conn = pymysql.connect(host="localhost", user="root", password="intel123", db="intel_project", charset='utf8')
    print("conn is", conn.host)
    cur = conn.cursor()
    sql = 'select car_number from car_number_mng;'

    cur.execute(sql)

    rows = cur.fetchall()
    print("test IS ", rows, "count is", len(rows))

    for x in rows:
        arr.append(x[0])
    
    print("arr IS ", arr)
    resp = make_response(jsonify(arr))
    return resp

#차량 번호 조회
@app.route('/car-number', methods=['GET', 'POST'])
def find_car_num():
    arr = []
    conn = pymysql.connect(host="localhost", user="root", password="intel123", db="intel_project", charset='utf8')
    print("conn is", conn.host)
    cur = conn.cursor()
    sql = 'select id, car_number, created_at from car_number_mng;'

    cur.execute(sql)

    rows = cur.fetchall()
    print("test IS ", rows, "count is", len(rows))

    for x, y, z in rows:
        arr.append((x, y, z))
    
    print("arr IS ", arr)
    resp = make_response(jsonify(arr))
    return resp

#차량 번호 추가
@app.route('/car-number/regist', methods=['POST'])
def regist_car_number():
    car_num = request.form['car_num']

    print("req is ", request.form['car_num'])
    
    insert =  'INSERT INTO car_number_mng \
    (car_number) VALUES (%s);'
    cur = conn.cursor()
    cur.execute(insert, car_num)
    conn.commit()

    return 'done'

@app.route('/car-number/delete', methods=['POST'])
def delete_car_number():

    print("req is ", request.get_json())
    
    delete =  'DELETE FROM car_number_mng \
    WHERE id IN (%s);'

    cur = conn.cursor()
    result = cur.execute(delete, request.get_json())
    print("result is ", result)
    conn.commit()
    print("result2 is ", result)
    return 'done'

@app.route('/car-pass-log', methods=['GET'])
def find_car_pass_log():
    arr = []
    conn = pymysql.connect(host="localhost", user="root", password="intel123", db="intel_project", charset='utf8')
    select = 'SELECT id, pi_id, car_number, time, frame_path, isblock, created_at \
    FROM car_pass_log;'

    print("select is ", select)
    cur = conn.cursor()
    cur.execute(select)
    result = cur.fetchall()
    print("result is ", result)

    for x, y, z, a, b, c in result:
        arr.append((x, y, z, a, b, c))
    print("arr is ", arr)
    resp = make_response(jsonify(arr))
    return resp

if __name__ == '__main__':
    app.run(host='10.10.14.2', port=4000, debug=True)
