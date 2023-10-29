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

sticky cookie 지시자를사용해 엔진엑스 플러스가 쿠키를 생성하고 추적하게 한다.  
해당 설정은 사용자가 지속적으로 특정 업스트림 서버에 연결되도록 쿠키를 생성해 추적한다.  

sticky 지시자를 cookie 매개변수와 함께 사용하면 사용자의 첫 번째 요청 수신 시 업스트림 서버 정보를 포함하는 쿠키를 생성한다.  
엔진엑스 플러스는 쿠키를 추적해 이어지는 사용자 요청을 같은 서버로 전달한다.  
cookie 매개변수의 첫 번째 항목은 쿠키 이름이고, 만료시간(expires), 도메인(domain), 경로(path), 사용자 측의 쿠키 사용 제한(secure), 쿠키 전송을 위한 프로토콜(httponly) 등을 지정할 수 있다.  

 - sticky 지시자 예시
    - 생성하는 쿠키의 이름은 affiniy이고, example.com 도메인에서 사용할 수 있다.
    - 쿠키는 1시간 후에 만료되며 HTTPS를 통해서만 주고받을 수 있다.
    - 사용자 브라우저에서 쿠키를 조작하지 못하도록 httponly를 지정하고 도메인의 모든 하위 경로에 대해 하도록 path 값을 지정한다.
```nginx
upstream backend {
    server backend1.example.com;
    server backend2.example.com;
    sticky cookie
           affinity
           expires=1h
           domain=.example.com
           httponly
           secure path=/;
}
```

<br/>

## 스티키 런(엔진엑스 플러스)

sticky learn 지시자로 업스트림 애플리케이션이 생성한 쿠키를 찾아내어 추적한다.  

애플리케이션이 세션 상태를 위한 쿠키를 별도로 사용하고 있다면 엔진엑스 플러스는 쿠키를 따로 생성하지 않고 요청이나 응답에 포함된 쿠키 이름과 값을 찾아 추적할 수 있다. 예를 들어, Java 애플리케이션은 기본적으로 jsessionid를 사용하고, PHP 애플리케이션은 phphsessionid를 사용한다.  
sticky 지시자에 learn 매개변수를 지정하고, 쿠키 추적을 위한 공유 메모리 영역은 zone 매개변수로 정의하며 이름과 크기를 지정한다.  
create 매개변수에는 업스트림 서버의 응답 헤더에서 찾을 쿠키 이름을 지정하고, lookup 매개변수에 지정한 사용자 쿠키 이름으로 이전에 저장해둔 세션값이 있는지 확인한다.  

 - 스티키 런 예시
    - 업스트림 서버의 응답 헤더 중 Set-cookie 헤더에서 이름이 cookiename인 쿠키를 찾아 추적한다.
    - 해당 값은 엔진엑스에 저장되고 사용자 요청 헤더에서 쿠키 이름이 같은 값이 확인되면 해당 세션을 가진 업스트림 서버로 요청을 전달한다.
    - 세션 고정 값은 2 메가바이트 용량으로 생성된 공유 메모리 영역에 저장되며 약 1만 6000개의 세션 정보를 저장할 수 있다.
```nginx
upstream backend {
    server backend1.example.com:8080;
    server backend2.example.com:8081;

    sticky learn
           create=$upstream_cookie_cookiename
           lookup=$cookie_cookiename
           zone=client_sessions:2m;
}
```

<br/>

## 스티키 라우팅(엔진엑스 플러스)

sticky 지시자를 route 매개변수와 함께 사용한다. 이때 사용자 요청을 특정 업스트림 서버로 보내려면 경로에 대한 매핑 정보를 포함하는 변수를 사용한다.  

때때로 정교하게 트래픽을 특정 서버로 보내야 하는 상황이 있을 수 있다.  
이러한 경우 sticky 지시자와 route 매개변수를 이용할 수 있다.  
스티키 라우팅은 정교한 추적이 가능하며, 고정된 서버로 요청을 보낼 수 있다.  

 - 스티키 라우팅 예시
    - 업스트림 서버가 자바 애플리케이션일 때 세션 ID 값을 추출하고, 이 값을 이용해 특정 업스트림 서버로 요청을 전달한다.
    - 첫 번째 map 블록은 사용자 요청 쿠키에서 jsessionid 값을 추출해 $route_cookie 변수에 할당한다.
    - 두 번째 map 블록은 URI에 jsessionid 값이 있으면 값을 확인해 $route_uri 변수에 할당한다.
    - route 매개변수와 함께 사용된 sticky 지시자는 변수 여러 개를 인수로 사용할 수 있다.
        - 쿠키에서 jsessionid 값을 추출하면 $route_cookie 변수값이 존재하므로 backend1 서버로 요청을 보낸다.
        - URI에서 값을 발견하면 backend2 서버로 요청을 보낸다.
```nginx
map $cookie_jsessionid $route_cookie {
    ~.+\.(?P<route>\w+)$ $route;
}

map $request_uri $route_uri {
    ~jsessionid=.+\.(?P<route>\w+)$ $route;
}

upstream backend {
    server backend1.example.com route=a;
    server backend2.example.com route=b;

    sticky route $route_cookie $route_uri;
}
```

<br/>

## 커넥션 드레이닝(엔진엑스 플러스)

 - 서버 유지보수가 필요하거나 서버를 종료해야 ㅏ는 상황에서 활성 사용자 세션이 남아 있는 엔진엑스 서버를 점진적으로 서비스에서 제외하기
    - 엔진엑스 플러스 API로 drain 매개변수를 보내 엔진엑스가 추적 중이 아닌 새로운 연결을 더는 업스트림 서버로 보내지 않도록 설정한다.
```bash
$ curl -X POST -d '{"drain":true}' 'http://nginx.local/api/3/http/upstreams/backend/servers/0'
{
    "id":0,
    "server":"172.17.0.3:80",
    "weight":1,
    "max_conns":0,
    "max_fails":1,
    "fail_timeout":"10s",
    ..
}
```

<br/>

## 수동적인 헬스 체크

수동 헬스 체크는 HTTP, TCP, UDP 부하 분산 구성의 server 지시자에 설정한다.  
수동적인 모니터링은 클라이언트의 요청이 엔진엑스를 경유해 업스트림 서버로 보내진 후 타임아웃이나 요청 실패가 발생하는지 확인한다.  

HTTP 헬스 체크 설정하기: https://oreil.ly/9xsNp  
TCP 헬스 체크 설정하기: https://oreil.ly/_2MK5  
UDP 헬스 체크 설정하기: https://oreil.ly/kEYQN  


 - 업스트림 서버의 상태를 수동적으로 확인하기
    - 해당 설정은 사용자 요청에 대한 업스트림 서버의 응답을 모니터링해 업스트림 서버의 상태를 수동으로 확인한다.
    - max_fails 매개변수는 헬스 체크의 최대 실패 횟수이다.
    - fail_timeout은 실패에 대한 타임아웃 값이다.
```nginx
upstream backend {
    server backend1.example.com:1234 max_fails=3 fail_timeout=3s;
    server backend2.example.com:1234 max_fails=3 fail_timeout=3s;
}
```

<br/>

## 능동적인 헬스 체크(엔진엑스 플러스)

엔진엑스 플러스는 수동 헬스 체크와 능동 헬스 체크를 지원한다.  

HTTP 헬스 체크 설정하기: https://oreil.ly/9xsNp  
TCP 헬스 체크 설정하기: https://oreil.ly/_2MK5  
UDP 헬스 체크 설정하기: https://oreil.ly/kEYQN  


 - 업스트림 서버의 상태를 능동적으로 확인하기
    - http 모듈을 사용하는 경우 location 블록에 health_check 지시자를 사용해 능동적으로 상태를 확인한다.
    - 업스트림 서버의 최상위(/) 경로로 2초마다 HTTP GET 요청을 보내 서버 상태를 확인한다.
        - 헬스 체크 설정은 HTTP GET 메서드만 사용할 수 있다. 이는 HTTP 메서드가 백엔드 서버 상태를 바꿔 헬스 체크 결과가 변화는 것을 방지하기 위함이다.
        - 업스트림 서버는 헬스 체크에 대해 5회 ㅇ녀속 정상적으로 응답하면 상태가 양호하다고 간주한다.
        - 헬스 체크가 2회 연속 실패하면 해당 업스트림 서버는 문제가 있다고 판단되며 업스트림 풀에서 제외된다.
        - match 블록은 status, header, body 지시자로 구성되며 지시자들은 비교 플래그를 제공한다.
```nginx
http {
    server {
        # ..
        location / {
            proxy_pass http://backend;
            health_check interval=2s
                         fails=2
                         passes=5
                         uri=/
                         match=welcome;
        }
    }
    # 응답 코드가 200이고 Content-Type이 "text/html" 이면서
    # 응답 바디에 "Welcome to nginx!" 문자열이 있는지 확인한다.
    match welcome {
        status 200;
        header Content-Type=text/html;
        body ~ "Welcome to nginx!";
    }
}
```

<br/>

## 슬로 스타트(엔진엑스 플러스)

슬로 스타트는 지정된 시간 동안 업스트림 서버로 전달하는 요청의 수를 점진적으로 늘려나가는 개념이다.  
서버 시작 직후에 연결 폭주 없이 데이터베이스 연결을 맺고 캐시를 쌓을 시간을 확보함으로써 애플리케이션은 서비스를 원할히 제공할 준비를 할 수 있다.  
엔진엑스 플러스에서만 제공되며 hash, ip_hash, random 부하분산 방식에서는 사용할 수 없다.  

 - 운영 환경에서 실사용자 트래픽을 받기 전에 애플리케이션의 예열이 필요한 상황
    - server 지시자에 slow_start 매개변수를 사용해 점진적으로 사용자 연결을 늘려나갈 시간 범위를 지정하고 업스트림 서버 부하분산 풀에 각 서버가 투입되도록 한다.
```nginx
upstream {
    zone backend 64k;

    server server1.example.com slow_start=20s;
    server server2.example.com slow_start=15s;
}
```
