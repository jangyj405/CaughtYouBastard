import sys
sys.path.insert(1,'../model/')
import socket
import json
from datetime import datetime
import pytz
import requests


def tcp_connection():
    HOST = "10.10.14.220"  # The server's hostname or IP address
    PORT = 5000  # The port used by the 
    clent_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    clent_socket.connect((HOST, PORT))

    return clent_socket

def send_log_data(socket, id, img, number):
    print("send to data test1")
    utc = pytz.timezone('UTC')
    kst = pytz.timezone('Asia/Seoul')

    utc_now = datetime.now(utc)
    kst_now = utc_now.astimezone(kst)
    print("send to data test12")
    LogData = {"id" : id }
    LogData["timeStamp"]=kst_now.strftime("%Y-%m-%d-%H-%M-%S")
    LogData["frame"]=img
    LogData["number"]=number
    LogData["block"]=1
    json_string = json.dumps(LogData)
    
    result = socket.sendall(bytes(json_string, encoding='utf-8'))
    return result

def free_tcp_sosket(socket):
    print("socket close")
    socket.close()

def get_car_num_list():
    resp = requests.get('http://10.10.14.220:8000/car-number-list')
    print("carnum is ", resp.text)

    result = resp.text

    return result