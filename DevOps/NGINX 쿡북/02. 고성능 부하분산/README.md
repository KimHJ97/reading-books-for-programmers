# 02장. 고성능 부하분산

오늘날 인터넷 서비스의 사용자 경험은 높은 성능와 가용성을 필요로 한다.  
이를 위해 일반적으로 같은 시스템을 여러 대 운영하고 부하를 각 시스템으로 분산한다.  
엔진엑스는 이러한 요구사항을 HTTP, TCP, UDP 프로토콜의 부하분산을 통해 충족한다.  

엔진엑스를 경유해 업스트림 서버로 전달되는 요청은 여러 이유로 언제든 실패할 수 있다.  
떄문에, 엔진엑스와 같은 프록시 혹은 로드 밸런서 서버는 업스트림 서버의 문제를 감지할 수 있어야 하며, 문제 발견시 트래픽 전송을 중지할 수 있어야 한다.  
엔진엑스는 업스트림 서버의 문제로 인한 서비스 품질 저하를 줄이는 방법으로 프록시 서버와 업스트림 서버의 상태를 확인하는 방법이 있다.  

엔진엑스는 두 가지 서버 상태 확인 방법을 제공한다.  
오픈 소스 버전은 패시브 방식, 엔진엑스 플러스는 패시브 및 액티브 방식을 제공한다.  
 - 패시브 방식: 사용자의 요청을 로드 밸런서가 받은 시점에 업스트림 서버와의 연결이나 응답을 확인하는 방식
 - 액티브 방식: 로드 밸런서 장비가 스스로 업스트림 서버와 주기적으로 연결을 시도하거나 요청을 보내 서버 응답에 문제가 없는지 확인하는 방식

<br/>

## HTTP 부하분산

HTTP upstream 모듈을 이용해 HTTP 프로토콜 요청에 대한 부하분산 방식을 정의한다.  
부하분산을 위한 목적지 풀은 유닉스 소켓, IP 주소, DNS 레코드 혹은 이들의 조합으로 구성한다.  
upstream 모델은 또한 개별 요청에 대해 어떤 업스트림 서버를 할당할지 매개변수로 정의한다.  

__엔진엑스의 upstream 블록과 http 모듈을 이용해 HTTP 서버 간에 부하를 분산한다.__  

 - 80 포트를 사용하는 HTTP 서버 두 대로 부하 분산
    - 설정한 서버 2대에 문제가 발생해 연결이 불가능하면 backup으로 지정한 서버를 사용한다.
    - weight 매개변수값에 따라 두 번쨰 서버는 첫 번째 서버보다 2배 많은 요청을 받게 된다. 기본값은 1이며 생략이 가능하다.
```nginx
upstream backend {
    server 10.10.12.45:80           weight=1;
    server app.example.com:80       weight=2;
    server spare.example.com:80     backup;
}
server {
    location / {
        proxy_pass http://backend;
    }
}
```

<br/>

## TCP 부하분산

http와 stream의 가장 큰 차이점은 두 모듈이 OSI 모델의 서로 다른 계층에서 동작한다는 점이다.  
http 컨텍스트는 OSI 모델의 7 계층인 애플리케이션 계층에서 동작하며 stream 컨텍스트는 4계층인 전송 계층에서 동작한다.  
http 모듈은 HTTP 프로토콜을 완전히 이해하도록 특별히 설계된 반면 stream 모듈은 패킷의 전달 경로 결정과 부하분산에 더 중점을 둔다.  

엔진엑스에서 TCP 부하분산은 stream 모듈을 이용해 정의하며, http 모듈과 마찬가지로 업스트림 서버 풀을 만들거나 수신할 개별 서버를 지정한다.  
서버가 특정 포트로 요청을 받게 하려면 수신할 포트를 설정에 추가하거나 IP 주소와 함께 포트 번호를 기술한다.  
또한, stream 모듈은 옵션을 통해 TCP 연결과 관계된 리버스 프록시의 여러 속성을 변경할 수 있는데, 유효한 SSL/TLS 인증서 제한, 타임아웃, 킬업라이브 시간 설정 등이 있다.  

__엔진엑스의 upstream 블록과 stream 모듈을 이용해 TCP 서버 간에 부하를 분산한다.__  

 - 3306 포트로 TCP 요청을 받아 읽기 전용 복제본 두 대로 구성된 MySQL 서버로 부하 분산
    - 만약, 지정한 MySQL 서버 두 대가 모두 다운되면 backup 매개변수로 지정한 서버로 요청이 전달된다.
    - stream 모듈을 이용한 설정은 stream.conf.d 라는 별도의 폴더를 생성해 저장하여 관리하는 것이 좋다. 경로를 nginx.conf 파일의 stream 블록에 추가해 엔진엑스가 참조하도록 한다.
```nginx
stream {
    upstream mysql_read {
        server read1.example.com:3306   weight=5;
        server read2.example.com:3306;
        server 10.10.12.34:3306         backup;
    }
    server {
        listen 3306;
        proxy_pass mysql_read;
    }
}
```

 - /etc/nginx/nginx.conf 설정 파일
```nginx
user nginx;
worker_process auto;
pid /run/nginx.pid;

stream {
    include /etc/nginx/stream.conf.d/*.conf;
}
```

 - /etc/nginx/stream.conf.d/mysql_read.conf
```nginx
upstream mysql_read {
    server read1.example.com:3306   weight=5;
    server read2.example.com:3306;
    server 10.10.12.34:3306         backup;
}
server {
    listen 3306;
    proxy_pass mysql_read;
}
```

<br/>

## UDP 부하분산

UDP 부하분산은 TCP와 마찬가지로 stream 모듈을 통해 설정하며, listen 지시자를 통해 UDP 데이터그램을 처리할 소켓을 지정한다.  
데이터그램을 다룰 때는 TCP 부하분산에서 사용하지 않는 지시자를 몇 가지 더 사용하게 된다.  
 - proxy_response: 업스트림 서버로부터 수신할 것으로 예상되는 응답의 크기 지정
 - proxy_timeout: 연결을 닫기 전에 목적지 서버로의 읽기, 쓰기 작업 완료를 기다리는 시간

__udp로 정의된 upstream 블록을 엔진엑스의 stream 모듈에서 사용해 UDP 서버 간에 부하를 분산한다.__  


 - UDP 프로토콜을 사용해 네트워크 타임 프로토콜 서버 두 대로 부하 전달
    - UDP 프로토콜의 부하분산 설정은 listen 지시자에 udp 매개변수만 추가하면 된다.
```nginx
stream {
    upstream ntp {
        server ntp1.example.com:123 weight=2;
        server ntp2.example.com:123;
    }

    server {
        listen 123 udp;
        proxy_pass ntp;
    }
}
```

 - 부하분산이 적용된 서비스에서 클라이언트와 서버 패킷을 여러 번 주고받아야 하는 경우
    - reuseport 매개변수 사용
```nginx
stream {
    server {
        listen 1195 udp reuseport;
        proxy_pass 127.0.0.1:1194;
    }
}
```

<br/>

## 부하분산 알고리즘

엔진엑스는 여러 가지의 부하분산 알고리즘을 제공한다.  
 - 지정된 서버의 순서에 따라 요청을 분산하는 라운드 로빈 [기본값]
 - 연결이 적은 서버를 먼저 활용하는 리스트 커넥션 (least_conn)
 - 응답 속도가 빠른 서버를 우선 사용하는 리스트 타임 (least_time) [Nginx + 에서만 사용 가능] 
 - 특정 문자열 기반 해시를 활용하는 제네릭 해시 (hash)
 - 임의 서버를 할당하는 랜덤 (random)
 - IP 주소 기반 해시를 사용하는 IP 해시 (ip_hash)

```nginx
upstream backend {
    least_conn;
    server backend.example.com;
    server backend2.example.com;
}
```

<br/>

## 스티키 쿠키(엔진엑스 플러스)