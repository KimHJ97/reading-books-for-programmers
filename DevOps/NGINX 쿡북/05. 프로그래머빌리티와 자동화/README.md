# 05장. 프로그래머빌리티와 자동화

프로그래머빌리티란 프로그래밍을 통해 상호 작용 하는 능력을 말한다.  
엔진엑스 플러스 API는 HTTP 요청을 통해 업스트림 서버를 추가하거나 삭제함으로써 엔진엑스 플러스를 재설정하게 해준다.  
또한, 엔진엑스 플러스가 제공하는 키-값 저장소는 HTTP 호출을 통해 엔진엑스 플러스에 정보를 주입하고 업스트림 경로나 트래픽을 제어해 한 단계 높은 수준의 동적인 설정 변경이 가능하도록 한다.  

<br/>

## 엔진엑스 플러스 API

 - 엔진엑스 플러스 API 호출로 서버 추가 및 삭제하기
```nginx
upstream backend {
    zone http_backend 64k;
}

server {
    # ..
    location /api {
        api     [write= on];
    }

    location = /dashboard.html {
        root    /usr/share/nginx/html;
    }
}
```

 - API 요청
    - 공식 문서: https://oreil.ly/BsdN5
```bash
# API로 업스트림 서버 추가
$ curl -X POST -d '{"server":"172.17.0.3"}' \ 
    'http://nginx.local/api/3/http/upstreams/backend/servers/'

# API로 업스트림 서버 정보 얻기
$ curl 'http://nginx.local/api/3/http/upstreams/backend/servers/'

# API로 서버 연결 종료
$ curl -X PATCH -d '{"drain":true}' \ 
    'http://nginx.local/api/3/http/upstreams/backend/servers/0'

# API로 서버를 업스트림 서버 풀에서 제외하기
$ curl -X DELETE 'http://nginx.local/api/3/http/upstreams/backend/servers/0'
```

<br/>

## NJS 모듈로 엔진엑스 자바스크립트 기능 활용하기

엔진엑스가 제공하는 NJS 모듈은 요청과 응답을 처리하는 동안 표준 자바스크립트를 사용할 수 있도록 해준다.  
이 모듈을 통해 필요한 비즈니스 로직을 프록시 계층에서 처리할 수 있다.  
NJS는 요청 수신뿐 아니라, 업스트림 서비스의 응답 데이터도 자바스크립트 로직을 통해 조작한 후 클라이언트에게 응답할 수 있다.  

 - njs 모듈 설치
    - NJS 스크립트 언어 공식 문서: https://oreil.ly/5NMAN
```Bash
# 데비안/우분투 환경
$ apt-get install nginx-module-njs
$ apt-get install nginx-plus-module-njs

# 레드햇/센트OS 환경
$ yum install nginx-module-njs
$ yum install nginx-plus-module-njs
```

 - /etc/nginx/njs/jwt.js 파일 생성
    - mkdir -p /etc/nginx/njs
    - JSON 웹 토큰(JWT)을 디코딩하는 함수와 이 함수를 이용해 JSON 웹 토큰에 포함된 특정 키를 획득하는 함수 정의
```JS
function jwt(data) {
    var parts = data.split('.').slice(0, 2)
                    .map(v => Buffer.from(v, 'base64url').toString())
                    .map(JSON.parse);
    return { headers:parts[0], payload: parts[1] };
}

function jwt_payload_subject(r) {
    return jwt(r.headersIn.Authorization.slice(7)).payload.sub;
}

function jwt_payload_issuer(r) {
    return jwt(r.headersIn.Authorization.slice(7)).payload.iss;
}

export default {jwt_payload_subject, jwt_payload_issuer}
```

 - NJS 모듈 사용 설정
    - NJS 모듈을 불러오고 자바스크립트 파일을 임포트한다. 엔진엑스 지시자들은 자바스크립트 함수가 반환한 값을 엔진엑스 변수에 설정한다.
```nginx
load_module /etc/nginx/modules/ngx_http_js_module.so;

http {
    js_path "/etc/nginx/njs/";
    js_import main from jwt.js;
    js_set $jwt_payload_subject main.jwt_payload_subject;
    js_set $jwt_payload_issuer main.jwt_payload_issuer;

    # ..

    server {
        listen 80 default_server;
        listen [::]:80 default_server;
        server_name _;
        location / {
            return 200 "$jwt_payload_subject $jwt_payload_issuer";
        }
    }
}
```

<br/>

## 앤서블로 엔진엑스 설치하기

앤서블은 파이썬으로 개발된 강력한 설정 관리 도구이다.  
YAML 형식으로 태스크를 설정하고 Jinja2 템플릿 언어를 사용해 파일을 템플릿화한다.  


 - 앤서블 갤럭시를 이용해 앤서블 엔진엑스 컬렉션 설치
    - 엔진엑스 공식 앤서블 컬렉션: https://galaxy.ansible.com/nginxinc/nginx_core
    - 앤서블 공식 문서: https://docs.ansible.com
```Bash
$ ansible-galaxy collection install nginxinc.nginx_core
```

 - 플레이북 작성
```playbook
---
 - hosts: all
   collections:
    - nginxinc.nginx_core
   tasks:
    - name: Install NGINX
      include_role:
        name: nginx
```
