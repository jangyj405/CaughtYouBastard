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

HOST = "10.10.14.2"  # Standard loopback interface address (localhost)
PORT = 8000  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = recvall(conn)
            print("data is", data, type(data))
            if not data:
                break
            json_string = data.decode(encoding="utf-8")

            try:
                dict = json.loads(data)

                print(dict["id"], dict["frame"],dict["number"],dict["timeStamp"],dict["block"],)
            except:
                pass
            #conn.sendall(data)