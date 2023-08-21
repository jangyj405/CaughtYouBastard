import json
import socket

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
            # either 0 or end of data
            break
    return data

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = recvall(conn)
            if not data:
                break
            json_string = data.decode()
            print(json_string)
            dict = json.loads(json_string)
            print(type(dict))
            print(dict["id"], dict["frame"],dict["number"],dict["timeStamp"],dict["block"],)
            conn.sendall(data)