import socket
import os
import sys
import json
import datetime
import jsonlines
import mysql.connector
import base64

HOST = "10.10.14.220"
PORT = 5000
BUF_SIZE = 1024

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
filename = "log" + ".jsonl"

with open(Dir+filename, 'r+') as f:
    filedata1 = f.read()
    f.close()

# 클라이언트와 연결
while True:
    # 클라이언트에서 파일 받기
    received = c_socket.recv(BUF_SIZE)
    received = received.decode("utf-8")
    print(received)

    with open(Dir+filename, 'a+') as f:
        f.write(received)
        f.flush()

        if not received:

            f.close()
            print("socket closed")
            break

# connect 종료
c_socket.close()

# json 파일 정리
with open(Dir+filename, 'r+') as f:
    filedata2 = f.read()
    f.close()

filedata = filedata2.replace("}{", "}\n{")

with open(Dir+filename, 'w+') as f:
    f.write(filedata)
    f.close()

print("file ready...")

# json을 tuple로 정리
pi_id = []
time = []
frame = []
car_number = []
isblock = []
with jsonlines.open(Dir+filename, 'r') as f:
    for line in f.iter():
        pi_id.append(line["id"])
        time.append(line["timeStamp"])
        frame.append(line["frame"])
        car_number.append(line["number"])
        isblock.append(line["block"])
print("list appended")

# frame 저장
Dir = r"/home/intel/webserver/pythonserver/cap/"
frame_path = []

for i in range(0, len(frame)):
    filename = f"car_{i}.jpeg"
    imgdata = base64.b64decode(frame[i])
    with open(Dir+filename, 'wb') as f:
        f.write(imgdata)
        f.close()
        frame_path.append(Dir+filename)


tupled = [(pi_id[i], car_number[i], time[i], frame_path[i], isblock[i]) for i in range(0, len(isblock))]

# mysql 연결
conn = mysql.connector.connect(host="localhost", user="root", password="intel123", db="rsbpi", charset="utf8")
cur = conn.cursor()

# 데이터 업로드
comm = "INSERT IGNORE INTO car_pass_log (pi_id, car_number, time, frame_path, isblock)\
 VALUES (%s, %s, %s, %s, %s);"
cur.executemany(comm, tupled)

conn.commit()

print("DB updated", cur.lastrowid)
conn.close()


