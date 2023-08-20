# 필요한 패키지 import
import socket # 소켓 프로그래밍에 필요한 API를 제공하는 모S
import json
# 서버 ip 주소 및 port 번호
ip = 'localhost'
port = 3333

# 소켓 객체 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    # 서버와 연결
    client_socket.connect((ip, port))
    
    print("연결 성공")
 
    image_dict = {
        "test_image": "test",
        "hi" : "hoo"
    }
    
    data = json.dumps(image_dict)

    client_socket.sendall(bytes(data, encoding='utf-8'))

        # sendall : 데이터(프레임) 전송
        # - 요청한 데이터의 모든 버퍼 내용을 전송
        # - 내부적으로 모두 전송할 때까지 send 호출
        # struct.pack : 바이트 객체로 반환
        # - > : 빅 엔디안(big endian)
        #   - 엔디안(endian) : 컴퓨터의 메모리와 같은 1차원의 공간에 여러 개의 연속된 대상을 배열하는 방법
        #   - 빅 엔디안(big endian) : 최상위 바이트부터 차례대로 저장
        # - L : 부호없는 긴 정수(unsigned long) 4 bytes
        #client_socket.sendall(struct.pack(">L", len(frame)) + frame)

# 메모리를 해제
#capture.release()