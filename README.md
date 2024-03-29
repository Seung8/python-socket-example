# 파이썬 소켓 프로그래밍

### 웹소켓

- 하나의 TCP 접속에 `전이중 통신` 채널을 제공하는 프로토콜이다.
- 소켓을 이용하면 통신은 오로지 소켓만을 이용하여 외부와 통신한다.

**통신방식**

```
단방향 통신: 어느 한 쪽에서 일방적으로 송신만 가능
반이중 통신: 어느 한 쪽에서는 송신하고 다른 한 쪽에서 수신
전이중 통신: 송신과 수신이 독립되어 각각 별개로 송수신이 가능
```

### Socket 객체

- BSD 소켓 인터페이스를 제공하며 해당 인터페이스는 UNIX, macOS, Window 등에서 사용할 수 있다.
- 운영체제의 Socket API를 호출하기 때문에 일부 운영체제에서는 동작이 다를 수 있다.
- socket() 함수는 첫 번째 인자로 Address Family(AF)와 Socket Type(Enum 형태의 Int값)을 받는다.
- socket() 함수 인자 Address Family와 Socket Type의 기본값은 각각 AF\_INET, SOCKET\_STREAM이다.
- 아래부터는 이해를 돕기위해 서버 소켓(요청 수신 및 응답)과 클라이언트 소켓(요청 송신)으로 나누어 설명한다.

### 서버 소켓

- 예시로 서버 소켓은 대기 소켓(수신 소켓)과 실제 통신을 담당하는 소켓(응답 소켓 또는 반환 소켓)으로 설정한다.
- 서버 소켓은 연결 요청을 대기하다가 연결을 수락할 경우 새로운 Socket 객체를 반환한다.
- 실제 외부와의 통신은 여기서 반환된 새로운 Socket 객체를 통해 통신한다.

#### socket.bind(address) - 소켓 맵핑

- 생성한 소켓에 고유한 호스트와 포트를 맵핑한다.
- 인자로 address(호스트와 포트 정보)를 튜플 형태를 전달 받는다. ex) socket.bind(('{host}', '{port}')
- Socket 객체(프로그램 인터페이스)에 고유한 네트워크 IP 자원(호스트와 포트)을 맵핑함으로써 프로그램 인터페이스와 네트워트 자원을 연결시킨다.

#### socket.listen() - 연결 요청 대기 상태 설정

- 소켓은 생성된 이후 연결 요청 대기를 한 이후에만 연결이 가능하므로 소켓 맵핑 후에는 반드시 연결 요청 대기 상태를 설정해야 한다.
- 연결 대기 상태는 오로지 대기(listen)만을 할 뿐 실제 연결이 성립되면 새로운 소켓을 반환한다.

#### socket.accept() - 연결 승낙 후 실제 통신 소켓 반환

- 연결 요청 대기 중인 소켓은 socket.accept()를 사용하여 연결을 승낙하고 연결이 성립된 새로운 소켓과 주소정보를 반환한다.
- 실제 외부와의 통신은 여기서 생성된 새로운 소켓을 이용한다.

#### socket.close() - 연결 요청 대기 종료

- socket.close()를 사용할 경우 해당 소켓은 종료된다.

### 클라이언트 소켓

클라이언트 소켓은 서버 소켓과 달리 오로지 클라이언트 소켓 하나로 구성된다.

#### socket.connet(address) - 서버 소켓에 연결 요청

- socket.connet()를 사용하여 서버 소켓에 연결 요청을 보낸다.
- 인자로 address(연결할 소켓의 호스트와 포트 정보)를 튜플 형태로 전달 받는다.
- 파이썬 3.5 버전 이후에서는 연결이 종료된 경우 InterruptedError에러나 socket.timeout없이 대기 상태로 전환된다.

### 서버 소켓과 클라이언트 소켓의 통신

서버 소켓과 클라이언트 소켓간 데이터 송수신을 설명한다.

#### socket.send(byte), socket.sendall(byte) - 데이터 송신

- 클라이언트 소켓에서 서버 소켓으로 데이터를 전송할 때는 socket.send() 혹은 socket.sendall()을 이용한다.
- 인자인 `byte`는 송신할 데이터를 의미한다.
- socket.send()와 socket.sendall()은 기본적으로 같은 역할을 하지만 sendall()의 경우는 전송이 완료된 데이터의 바이트 수를 리턴한다.

#### socket.recv(bufsize) - 데이터 수신

- 데이터를 수신할 때 사용되며 수신한 데이터(바이트 객체)를 반환한다.
- 인자인 `bufsize`는 한 번에 수신할 수 있는 최대 데이터의 크기를 의미한다.


### 파이썬으로 소켓 실습

- [파이썬 socket 공식문서](https://docs.python.org/3/library/socket.html#example) 예제를 기반으로 실습

**server socket**

```python
import socket

# 소켓 접속 시 허용할 호스트
HOST = '127.0.0.1'
# 소켓 접속 시 허용할 포트
PORT = 50007

# 소켓 생성
with socket.socket(socket.AF\_INET, socket.SOCK\_STREAM) as s:
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
```

**client socket**

```python
import socket

# 접속할 서버 소켓의 호스트
HOST = '127.0.0.1'
# 접속할 서버 소켓의 포트
PORT = 50007

# 클라이언트 소켓 생성
with socket.socket(socket.AF\_INET, socket.SOCK\_STREAM) as s:
    # 서버 소켓의 HOST:PORT로 연결한다.
    s.connect((HOST, PORT))
    # sendall을 통해 연결된 소켓에 바이트 데이터를 전송한다.
    s.sendall(b'Hello, world')
    # 연결한 소켓으로부터 최대 1024바이트의 데이터를 수신하여 data 변수에 할당한다.
    data = s.recv(1024)
print('Received', repr(data))
```
