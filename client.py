import socket

# 접속할 서버 소켓의 호스트
HOST = '127.0.0.1'
# 접속할 서버 소켓의 포트
PORT = 50007

# 클라이언트 소켓 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 서버 소켓의 HOST:PORT로 연결한다.
    s.connect((HOST, PORT))
    # sendall을 통해 연결된 소켓에 바이트 데이터를 전송한다.
    s.sendall(b'Hello, world')
    # 연결한 소켓으로부터 최대 1024바이트의 데이터를 수신하여 data 변수에 할당한다.
    data = s.recv(1024)
print('Received', repr(data))