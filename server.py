import socket

# 소켓 접속 시 허용할 호스트
HOST = '127.0.0.1'
# 소켓 접속 시 허용할 포트
PORT = 50007

# 소켓 생성
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    # 생성한 소켓에 설정한 HOST와 PORT를 맵핑한다.
    s.bind((HOST, PORT))
    # 맵핑된 소켓을 연결 요청 대기 상태로 전환한다.
    s.listen(1)
    # 실제 소켓 연결 시 반환되는 실제 통신용 연결된 소켓 conn과 연결 주소인 addr을 할당
    conn, addr = s.accept()
    
    # 실제 외부와 통신할 conn 소켓객체의 역할 설정
    with conn:
        # 연결 완료 프린팅
        print('연결됨 {}:{}'.format(addr[0], addr[1]))
        # 데이터 수신(receive)
        while True:
            # 연결한 소켓으로부터 최대 1024바이트의 데이터를 수신하여 data 변수에 할당한다.
            data = conn.recv(1024)
            print('데이터 수신: {}'.format(str(data)))
            if not data: break