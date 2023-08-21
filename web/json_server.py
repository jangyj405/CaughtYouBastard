import socket
import os
import sys
import json
import datetime
import jsonlines

HOST = "10.10.14.220"
PORT = 8000
BUF_SIZE = 65535

now = datetime.datetime.now().strftime("%d-%H-%M-%S")

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

s_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("socket created")

try:
    s_socket.bind((HOST, PORT))
except socket.error:
    print("bind failed")

s_socket.listen(5)
print("socket awaiting")

c_socket, addr = s_socket.accept()
print("connected by", addr)

Dir = r"/home/intel/webserver/pythonserver/json/"
filename = "log_" + now + ".jsonl"

# 클라이언트와 연결
while True:
    # 클라이언트에서 파일 받기

    received = c_socket.recv(BUF_SIZE)
    received = received.decode("utf-8")
    print(received)

    with open(Dir+filename, 'a') as f:
        f.write(received)
        f.flush()

        if not received:
            f.close()
            print("json accepted")
            break
'''
    data = recvall(c_socket, 32)
    if not data:
        break
    json_string = data.decode(encoding="utf-8")

    try:
        dict = json.loads(data)

        print(dict["id"])

    except:
        pass
'''
# connect 종료
c_socket.close()

'''
json_data = []
with open(Dir+filename, 'r') as f:
    for line in f:
        json_data.append(json.loads(line))
    json_obj = json.load(f)
    car_number = json_obj['car_number']
    print(car_number)
'''

car_number = []
with jsonlines.open(Dir+filename, 'r') as f:
    for line in f.iter():
        car_number.append(line["car_number"])

print(car_number)


conn = pymysql.connect(host="localhost", user="root", password="intel123", db="rsbpi", charset="utf8")
cur = conn.cursor()

#cur.execute("SELECT id, datetime, frame, number, block\
#from car_number_")




#new_num = received['car_number']
#print("this is ", new_num)
#comm = "INSERT INTO car_number_mng (car_number) values (%s);"
#cur.execute(comm, new_num)
#print("DB updated")

#conn.commit()
conn.close()
