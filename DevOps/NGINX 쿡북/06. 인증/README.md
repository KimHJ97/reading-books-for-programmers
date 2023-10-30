# 06장. 인증

엔진엑스는 클라이언트에 대한 인증을 수행할 수 있다.  
클라이언트 요청을 엔진엑스가 인증함으로써 업스트림 서버에서 인증을 처리하며 발생하는 부하를 줄이고 동시에 인증받지 못한 요청이 애플리케이션 서버까지 도달하는 것을 막을 수 있다.  
엔진엑스 오픈 소스 버전에서 사용할 수 있는 인증 모듈에는 HTTP 기본 인증과 하위 요청을 통한 인증이 있다.  
엔진엑스 플러스에서는 JWT 검증 모듈을 사용가능하며, 표준 오픈 아이디 커넥트 인증을 제공하는 서드파티 인증 사업자들을 엔진엑스로 통합한다.  

<br/>

## HTTP 기본 인증

 - 사용자 정보 기록 파일 생성
    - 1 번쨰 필드는 사용자 이름이고, 2 번째 필드는 비밀번호이다. 3 번쨰 필드는 기록할 내용이다. (각 필드는 콜론으로 구분한다.)
    - 엔진엑스는 몇 가지 비밀번호 형식을 지원하는데 대표적으로 C언어에서 제공하는 crypt() 함수로 암호화된 비밀번호가 있다. openssl을 통해 passwd 명령도 내부적으로 crypt()를 이용한다.
        - $ openssl passwd MyPassword1234
```
name1:password1
name2:password2:comment
```

 - NGINX 설정
    - curl 명령의 -u 혹은 --user 옵션으로 사용자 이름과 비밀번호에 대한 Authorization 인증 헤더를 만들어 보낸다.
    - $ curl --user myuser:MyPassword1234 https://localhost
```nginx
location / {
    auth_basic      "Private Site";
    auth_basic_user_file conf.d/passwd;
}
```

<br/>

## 인증을 위한 하위 요청

http_auth_request_module은 엔진엑스 서버가 처리하는 모든 요청에 대해 인증을 받도록 한다.  
사용자 요청을 처리해도 괜찮은지 확인하기 위해 하위 요청을 보내고 인증 시스템으로부터 인증을 받는다.  

 - 서드파티 인증 시스템을 통해 사용자 요청 인증하기
    - 요청된 리소스에 대해 응답하기 전에 http_auth_request_module을 사용해 인증 서비스로 요청을 보내고 사용자의 ID를 확인한다.
        - auth_request 지시자의 매개변수로 내부 인증 시스템의 위치를 가리키는 URI를 지정한다.
        - auth_request_set 지시자는 인증을 위한 하위 요청의 응답으로 받은 값을 매개변수에 지정된 변수에 저장한다.
```nginx
location /private/ {
    auth_request        /auth;
    auth_request_set    $auth_status $upstream_status;
}

location = /auth {
    internal;
    proxy_pass                  http://auth-server;
    proxy_pass_request_body     off;
    proxy_set_header            Content-Length "";
    proxy_set_header            X-Original-URI $request_uri;
}
```

<br/>

## JWT 검증하기(엔진엑스 플러스)


 - 사용자 요청을 업스트림 서버로 보내기 전에 JWT 검증하기
    - 엔진엑스 플러스의 JWT 인증 모듈을 사용해 토큰의 시그니처를 검증하고 JWT 속성 정보와 헤더를 엔진엑스 변수로 가져온다.
```nginx
location /api/ {
    auth_jwt                "api";
    auth_jwt_key_file       /conf/keys.json;
}
```
