import json
import socket
from datetime import datetime, timezone
import pytz

utc = pytz.timezone('UTC')
kst = pytz.timezone('Asia/Seoul')

utc_now = datetime.now(utc)
kst_now = utc_now.astimezone(kst)

LogData = {"id" : 0, }
LogData["timeStamp"]=kst_now.strftime("%Y-%m-%d-%H-%M-%S")
LogData["frame"]="frame"
LogData["number"]="1234"
LogData["block"]=1

json_string = json.dumps(LogData)
json_byte = str.encode(json_string)
print(json_string)
print(type(json_byte))


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(json_byte)
    data = s.recv(1024)

print(f"Received {data!r}")





