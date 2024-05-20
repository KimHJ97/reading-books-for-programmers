# 08장. HTTP/2

HTTP/2는 HTTP 프로토콜의 주요 개정판으로 단일 TCP 연결을 통한 모든 요청과 응답의 멀티플렉싱같은 전송 계층 변화에 집중되어 있다.  
HTTP 헤더 압축을 통해 트래픽을 보다 효율적으로 전송하고 각 요청에 중요도를 부여할 수 있게 됐으며, 그 외에도 서버가 요청받지 않은 리소스도 클라이언트로 보낼 수 있도록 서버 푸시에 대한 지원이 추가되었다.  

<br/>

## 기본 설정

HTTP/2를 활성화하기 위해 listen 지시자에 http2 매개변수를 추가한다.  

 - 엔진엑스 HTTP/2 활성화
```nginx
server {
    listen 443 ssl http2 default_server;
    ssl_certificate server.crt;
    ssl_certificate_key server.key;
}
```

<br/>

## gRPC

 - gRPC 메서드 호출 종결, 분석, 전달, 부하 분산
    - 암호화되지 않은 HTTP/2 트래픽을 80포트로 수신하고, 50051 포트를 사용하는 backend.local 서버로 요청을 프록시한다.
    - grpc_pass 지시자는 엔진엑스가 사용자 요청을 gRPC 호출로 다루도록 한다.
```nginx
server {
    listen 80 http2;
    location / {
        grpc_pass grpc://backend.local:50051;
    }
}
```

 - gRPC TLS 암호화 활용
    - 엔진엑스에서 TLS 세션을 종료시키고 암호화되지 않은 HTTP/2 연결을 사용해 업스트림 애플리케이션으로 gRPC 통신 수행
    - 클라이언트와 엔진엑스 구간에서 TLS 암호화를 활용하면서 사용자 요청을 애플리케이션 서버로 보내기 전에 TLS 세션을 종료시킨다.
        - 만약, gRPC 통신에 종단간 트래픽 암호화를 제공하도록 하려면 'grpc_pass://도메인'를 'grpcs_pass://도메인'로 사용한다.
```nginx
server {
    listen 443 ssl http2 default_server;
    ssl_certificate     server.crt;
    ssl_certificate_key server.key;
    location / {
        grpc_pass grpc://backend.local:50051;
    }
}
```

 - gRPC URI 요청 전달
    - 패키지, 서비스, 메서드가 포함된 gRPC URI에 따라 서로 다른 백엔드 서비스로 요청을 전달할 수 있다.
    - 아래 설정은 location 지시자를 사용해 수신하는 HTTP/2 트래픽을 경로에 따라 서로 다른 gRPC 서비스로 전달하며 정적인 콘텐츠는 별도의 location 분기를 통해 제공한다.
```
location /mypackage.service1 {
    grpc_pass grpc://$grpc_service1;
}
location /mypackage.service2 {
    grpc_pass grpc://$grpc_service2;
}
location / {
    root /usr/share/nginx/html;
    index index.html index.htm;
}
```

 - gRPC 요청 부하분산
    - upstream 블록은 gRPC에 대해서도 HTTP 트래픽에 대한 방식과 동일하게 동작한다. 단, grpc_pass 지시자를 통해 upstream을 참조한다.
```nginx
upstream grpcservers {
    server backend1.local:50051; server backend2.local:50051;
}

server {
    listen 443 ssl http2 default_server;
    ssl_certificate     server.crt;
    ssl_certificate_key server.key;
    location / {
        grpc_pass grpc://grpcservers;
    }
}
```

<br/>

## HTTP/2 서버 푸시

 - 클라이언트에 콘텐츠 즉시 전송하기
    - HTTP/2 서버 푸시를 사용하려면 서버가 HTTP/2를 사용하도록 설정한다.
    - http2_push 지시자를 사용해 엔진엑스가 특정 파일을 선점적으로 클라이언트에 보내도록 할 수 있다. 매개변수로는 전달할 파일의 전체 URI 경로를 받는다.
```nginx
server {
    listen 443 ssl http2 default_server;
    ssl_certificate     server.crt;
    ssl_certificate_key server.key;
    root /usr/share/nginx/html;
    location = /demo.html {
        http2_push /style.css;
        http2_push /image1.jpg;
    }
}
```
