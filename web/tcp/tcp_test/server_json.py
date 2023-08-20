# 서버 프로그램 (TCP)
import socket, time
import json
import base64
import pickle
host = 'localhost' # 서버 컴퓨터의 ip(여기선 내 컴퓨터를 서버 컴퓨터로 사용) 
                   # 본인의 ip주소 넣어도 됨(확인방법: cmd -> ipconfig)
port = 3333  # 서버 포트번호(다른 프로그램이 사용하지 않는 포트번호로 지정해야 함)

# https://stackoverflow.com/questions/39817641/how-to-send-a-json-object-using-tcp-socket-in-python

# 서버소켓 오픈(대문을 열어둠)
# socket.AF_INET: 주소종류 지정(IP) / socket.SOCK_STREAM: 통신종류 지정(UDP, TCP)
# SOCK_STREAM은 TCP를 쓰겠다는 의미
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 여러번 ip.port를 바인드하면 에러가 나므로, 이를 방지하기 위한 설정이 필요
# socket.SOL_SOCKET: 소켓 옵션
# SO_REUSEADDR 옵션은 현재 사용 중인 ip/포트번호를 재사용할 수 있다.
# 커널이 소켓을 사용하는 중에도 계속해서 사용할 수 있다
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# server socket에 ip와 port를 붙여줌(바인드)
server_socket.bind((host, port))

# 클라이언트 접속 준비 완료
server_socket.listen()

print('echo server start') # echo program: 입력한 값을 메아리치는 기능(그대로 다시 보냄)

# accept(): 클라이언트 접속 기다리며 대기
# 클라이언트가 접속하면 서버-클라이언트 1:1 통신이 가능한 작은 소켓(client_soc)을 만들어서 반환
# 접속한 클라이언트의 주소(addr) 역시 반환
conn, addr = server_socket.accept()

print("conn is ", conn)
print('connected client addr:', addr)

data_size = 5000#struct.unpack('>I', conn.recv(4))[0]
print("data_size is ", data_size)

received_payload = b""
print("received_payload is ", received_payload)

reamining_payload_size = data_size
#while reamining_payload_size != 0:
received_payload += conn.recv(100)
print("received_payload is", received_payload)
#reamining_payload_size = data_size - len(received_payload)

my_json = received_payload
print(my_json)
print('- ' * 20)
data = json.loads(my_json)
s = json.dumps(data, indent=4, sort_keys=True)

with open('test.pickle', 'wb') as ofp:
    pickle.dump(received_payload, ofp)
    #ofp.write(received_payload[:10])


with open('test.pickle', 'rb') as ifp:
    data = pickle.load(ifp)
    print("r is ", data, type(data))

    print(s)
#with open('test2.pkl', 'rb') as my_file:
#    hohoho = pickle.load(my_file)
#    print("hohoho is ", hohoho)



#print("result is ", dw)
#client_soc.sendall(msg.encode(encoding='utf-8')) # 에코메세지 클라이언트로 보냄

time.sleep(5)
server_socket.close() # 사용했던 서버 소켓을 닫아줌