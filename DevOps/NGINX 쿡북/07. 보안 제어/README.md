# 07장. 보안 제어

## IP 주소 기반 접근 제어

 - 클라이언트의 IP 주소를 사용해 접근 제어하기
    - 사용자가 IPv4 주소를 사용하면 10.0.0.0/20 대역의 접근을 허용하며, IPv6 주소를 사용하면 2001:0db8::/32 대역의 접근을 허용한다.
    - IPv4 주소가 10.0.0.1 이면 접근을 차단하며 그 외에 기술되지 않은 IPv4, IPv6 주소의 접근은 차단돼 403 응답을 반환한다.
```nginx
location /admin/ {
    deny 10.0.0.1;
    allow 10.0.0.0/20;
    allow 2001:0db8::/32;
    deny all;
}
```

<br/>

## 크로스 오리진 리소스 공유(CORS)

 - CORS 접근 허용(사용자 요청 메서드에 따라 응답 헤더 변경)
    - map 지시자를 사용해 GET, POST 메서드를 그룹화해 처리한다. OPTIONS 메서드는 프리플라이트 요청으로 사용자에게 서버가 가진 CORS 정책을 응답한다.
    - Allow-Methods로 GET, POST, OPTIONS 메서드를 허용한다.
    - Allow-Origin로 http://example.com의 여러 하위 도메인에서 서버 리소스에 접근 가능하도록 한다.
    - 프리플라이트 요청을 매번 보내지 않고도 CORS 정책을 참고할 수 있도록 사용자 브라우저에 Access-Control-Max-Age 헤더에 172만 8000초(20일)을 설정해 정책을 캐시한다.
```nginx
map $request_method $cors_method {
    OPTIONS 11;
    GET      1;
    POST     1;
    default  0;
}

server {
    # ..
    location / {
        if ($cors_method ~ '1') {
            add_header 'Access-Controll-Allow-Methods' 'GET,POST,OPTIONS';
            add_header 'Access-Controll-Allow-Origin' '*.example.com';
            add_header 'Access-Controll-Allow-Headers'
                       'DNT,
                        Keep-Alive,
                        User-Agent,
                        X-Requested-With,
                        If-Modified-Since,
                        Cache-Control,
                        Content-Type';
        }
        if ($cors_method = '11') {
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=UTF-8';
            add_header 'Content-Length' 0;
            return 204;
        }
    }
}
```

<br/>

## 클라이언트 측 암호화

 - 클라이언트와 엔진엑스 서버 간 트래픽 암호화하기
    - ngx_http_ssl_module이나 ngx_stream_ssl_module과 같은 SSL 모듈을 사용해 트래픽을 암호화한다.
    - 아래 설정은 서버가 8443 포트로 들어오는 요청에 대해 SSL/TLS를 사용해 암호화하도록 한다.
        - ssl_certificate 지시자는 인증서와 중간 체인 인증서가 저장된 파일 경로를 정의한다.
        - ssl_certificate_key 지시자는 엔진엑스가 클라이언트 요청을 복호화하고 응답을 암호화하는 데 사용할 비밀키 파일을 정의한다.
```nginx
http {
    server {
        listen 8443 ssl;
        ssl_certificate /etc/nginx/ssl/example.crt;
        ssl_certificate_key /etc/nginx/ssl/example.key;
    }
}
```

<br/>

## 고급 클라이언트 측 암호화

 - 클라이언트 암호화 높은 수준으로 설정하기
```nginx
http {
    server {
        listen 8443 ssl;

        # 허용할 TLS 버전과 암호화 알고리즘 설정
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5; # 암호화 수준 HIGH, aNULL과 MD5는 사용 X

        # RSA 인증서 및 키 파일 경로 지정
        ssl_certificate /etc/nginx/ssl/example.crt;
        ssl_certificate_key /etc/nginx/ssl/example.pem;

        # EV(Elliptic Curve) 인증서를 변수에서 불러온다.
        ssl_certificate $ecdsa_cert;
        # EV(Elliptic Curve) 키를 파일 경로가 담긴 변수를 참조해 읽어온다.
        ssl_certificate_key data:$ecdsa_key_path;

        # 클라이언트-서버 간의 SSL/TLS 연결 협상 결과 캐시
        ssl_session_cache shared:SSL:10m;
        ssl_session_timeout 10m;
    }
}
```

<br/>

## 업스트림 암호화

HTTP 프록시 모듈에서는 매우 다양한 지시자를 활용할 수 있으며 업스트림 트래픽을 암호화하기 위해서는 proxy_ssl_verify 옵션을 활성화해야 한다.  
HTTPS를 통해 요청을 프록시 하려면 proxy_pass 지시자에 전달하는 값에 HTTPS 프로토콜을 사용하도록 지정한다.  
하지만, 이것만으로는 업스트림 서버가 사용하는 인증서에 대한 검증을 수행하지 않고, 통신 구간의 보안 수준을 높이려면 proxy_ssl_certificate, proxy_ssl_certificate_key와 ㅏㄱㅌ은 지시자로 보안 요건을 지정한다.  

 - SSL 요구사항 지정
    - proxy 지시자들을 이용해 엔진엑스가 준수해야 하는 SSL 규칙을 정의한다.
    - 아래 설정은 엔진엑스가 업스트림 서비스의 서버 인증서와 인증서 체인이 두 단계까지 유효한지 확인한다.
    - proxy_ssl_protocols 지시자는 TLS 1.2 버전만 SSL 연결 설정에 사용하도록 설정한다. 기본적으로 엔진엑스는 업스트림 서비스의 인증서와 연결할 때 사용한 TLS 버전을 확인하지 않는다.
```nginx
location / {
    proxy_pass https://upstream.example.com;
    proxy_ssl_verify on;
    proxy_ssl_verify_depth 2;
    proxy_ssl_protocols TLSv1.2;
}
```

<br/>

## location 블록 보호하기

 - 비밀값을 활용해 location 블록 보호
    - 아래 설정은 공개된 location 블록과 내부에서만 접근 가능한 location 블록을 만든다.
    - /resources 경로에 대해 설정된 공개 location 블록은 요청 URI가 secure_link_secret 지시자에 설정된 비밀값으로 검증 가능한 MD5 해시값을 갖고 있지 않으면 '403 Forbidden'을 응답한다.
    - $secure_link 변수는 URI에 포함된 해시값이 검증되기 전까지는 아무런 값을 갖지 않는다.
```nginx
location /resources {
    secure_link_secret mySecret;
    if ($secure_link = "") { # 암호화된 보안 링크가 요청에 없으면 액세스 거부
        return 403;
    }

    rewrite ^ /secured/$secure_link; # 보안 링크가 올바르게 확인되면 요청된 URL 재작성 (/resources -> /secured/)
}

location /secured/ {
    internal; # 해당 블록을 내부 블록으로, 외부 클라이언트에게 직접 액세스 할 수 없도록 보호되는 리소스 경로 지정
    root /var/www;
}
```

<br/>

## HTTPS 리다이렉션

 - HTTP로 수신된 요청을 HTTPS로 리다이렉트하기
    - 아래 설정은 엔진엑스에 설정된 모든 호스트명에 대해 IPv4와 IPv6 주소를 가리지 않고 80 포트로 요청을 받는다.
    - return 구문은 클라이언트로 '301 Permanent Redirect' 응답을 보내 동일한 호스트명과 URI에 대해 다시 HTTPS로 요청하도록 한다.
```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 301 https://$host$request_uri;
}
```

<br/>

## HTTPS 리다이렉션 - SSL 오프로딩 계층이 있는 경우

 - SSL 오프로딩을 수행하는 상황에서 모든 사용자 요청을 HTTPS로 리다이렉트하기
    - 엔진엑스가 실제 사용자의 요청을 수신하는 경우가 아니라면 X-Forwarded-Proto 헤더를 통해 사용자의 프로토콜을 확인할 수 있으며 이 값을 활용해 리다이렉트한다.
```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;

    if ($http_x_forwarded_proto = 'http') {
        return 301 https://$host$request_uri;
    }
}
```

<br/>

## HSTS

 - 웹 브라우저가 HTTP로 요청을 보내지 않도록 강제하기
    - Strict-Transport-Security 헤더를 설정해 HSTS 확장을 사용한다.
    - 아래 설정은 Strict-Transport-Security 헤더를 유효 기간 1년(31,536,000초)으로 지정해 응답 헤더를 전달한다. 브라우저는 이 도메인에 대해 HTTP 요청이 발생하면 내부 리다이렉트를 통해 모든 요청이 항상 HTTPS를 이용하도록 한다.
```nginx
add_header Strict-Transport-Security max-age=31536000;
```

<br/>

## 다중 계층 보안

 - 폐쇄형 웹사이트를 위해 여러 계층의 보안 적용하기
    - satisfy 지시자를 사용해 모든 보안 검증을 통과해야만 요청을 허용할지 혹은 일부 보안 검증만 통과해도 유효한 요청으로 볼지 설정한다.
    - 아래 설정은 루트 경로에 대한 사용자 요청이 설정된 보안 검증 방법 중 하나 이상을 만족하면 유효한 요청으로 판단한다.
        - 사용자 IP 주소가 192.168.1.0/24 대역에서 접근
        - 서버릐 conf/htpasswd 파일에 설정된 계정 및 비밀번호와 일치
```nginx
location / {
    satisfy any;

    allow 192.168.1.0/24;
    deny all;

    auth_basic              "closed site";
    auth_basic_user_file    conf/htpasswd;
}
```

<br/>

## 다중 계층 DDoS 방어(엔진엑스 플러스)

 - 분산 서비스 거부 공격(DDoS) 완화하기
    - 엔진엑스 플러스를 사용해 클러스터 레벨의 빈도 제한과 자동화된 차단 리스트를 적용한다.
```nginx
# 클러스터 단위로 빈도 제한 적용
limit_req_zone $remote_addr zone=per_ip:1M rate=100r/s sync;
limit_req_status 429;

# TTL이 10분인 클러스터 단위의 sinbin 저장 영역을 만들고, 해당 영역에 사용자 IP 저장
keyval_zone zone=sinbin:1M timeout=600 sync;
keyval $remote_addr $in_sinbin zone=sinbin;

server {
    listen 80;
    location / {
        if ($in_sinbin) {
            set $limit_rate 50; # IP별 대역폭 제한 설정
        }

        # IP 단위 제한 적용
        limit_req zone=per_ip;

        # 빈도를 초과한 요청은 @send_to_sinbin으로 보내고, 문제가 없으면 my_backend로 보낸다.
        error_page 429 = @send_to_sinbin;
        proxy_pass http://my_backend;
    }

    location @send_to_sinbin {
        # 초과된 요청을 보낸 IP에 대해 sinbin 저장소에 플래그 설정
        rewrite ^ /api/3/http/keyvals/sinbin break;
        proxy_method POST;
        proxy_set_body '{"$remote_addr":"1"}';
        proxy_pass http://127.0.0.1:80;
    }

    location /api/ {
        # API 접근 제어
        api write=on;
    }
}
```

