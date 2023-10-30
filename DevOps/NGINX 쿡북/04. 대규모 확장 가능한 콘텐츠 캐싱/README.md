# 04장. 대규모 확장 가능한 콘텐츠 캐싱

캐싱은 다시 제공해야 하는 응답을 저장해뒀다가 빠르게 콘텐츠를 제공하는 방법이다.  
콘텐츠 캐싱은 업스트림 서버가 동일한 요청에 대해 계산이나 질의를 다시 수행하지 않도록 전체 응답을 저장함으로써 업스트림 서버의 부하를 낮춘다.  
캐싱을 통해 성능을 높이고 부하를 낮추면 더 적은 리소스로도 더 빠르게 콘텐츠를 제공할 수 있으며, 캐싱 서버를 전략적인 위치에 확대, 분산 배치해 사용자 경험을 개선할 수 있다.  

엔진엑스 캐싱을 통해 수동적으로 콘텐츠를 캐싱할 뿐 아니라 업스트림 서버에 문제가 생기면 캐싱된 응답으로 사용자에게 콘텐츠를 제공할 수 있다.  
캐싱 기능은 http 컨텍스트 내에서만 사용할 수 있다.  

<br/>

## 캐시 영역

엔진엑스에 캐싱을 설정하려면 캐시를 저장할 경로와 캐시 영역을 지정한다.  
proxy_cache_path 지시자로 캐시 정보를 저장할 위치와 활성화된 캐시 키 및 응답에 대한 메타데이터 정보를 저장할 공유 메모리 영역을 지정한다.  
levels로 캐시 파일을 저장할 디렉토리 구조를 어떻게 생성할지 정의한다.  
inactive로 마지막 요청 이후 오랫동안 요청되지 않더라도 캐시를 보관할 기간을 결정한다.  
max_size로 저장 가능한 캐시의 총 용량을 설정한다.  

 - 콘텐츠를 캐시하고 캐시를 어디에 저장할지 결정하기
    - proxy_catch_path 지시자를 사용해 공유 메모리 캐시 영역을 정의하고 콘텐츠 위치를 지정한다.
    - /var/nginx/cache 디렉토리를 생성하고 메모리에 CACHE라는 공유 메모리 영역을 60 메가바이트 크기로 생성한다.
    - 또한, 디렉토리 구조의 레벨을 지정하며 캐시 후 3시간 동안 해당 응답에 대한 요청이 없으면 캐시를 비활성화한다.
    - max_size: 캐시 영역의 크기가 20 GB가 넘지 않도록 지정한다.
    - proxy_cache_path는 http 컨텍스트에서만 유효하며, proxy_cache 지시자는 http, server, location 컨텍스트에서 사용 가능하다.
```nginx
proxy_cache_path /var/nginx/cache
                 keys_zone=CACHE:60m
                 levels=1:2
                 inactive=3h
                 max_size=20g;
proxy_cache CACHE;
```

<br/>

## 캐시 락

 - 생성 중인 캐시에 대한 요청은 업스트림 서버로 프록시하지 않기
    - proxy_cache_lock 지시자는 동일한 리소스에 대한 요청이 여러 개 들어오면 한 번에 하나의 요청을 통해서만 캐시가 만들어지도록 한다.
    - 캐시가 만들어지는 동안 수신된 요청은 가장 먼저 도착한 요청으로 캐시가 생성될 때까지 처리되지 않고 기다린다.
```nginx
proxy_cache_lock on;
proxy_cache_lock_age 10s; # 대기 시간, 시간 초과시 대기 중인 다른 요청을 업스트림 서버로 보내 응답 결과 캐시를 다시 시도
proxy_cache_lock_timeout 3s; # 캐시 생성 완료되지 않으면, 다른 요청을 업스트림 서버로 보내 필요한 콘텐츠를 가져온다. (캐시 생성은 X)
```

<br/>

## 해시 키 값 캐시

proxy_cache_key의 기본값은 "$scheme$proxy_host$request_uri"로 일반적으로 사용할 수 있다.  
$scheme는 HTTP나 HTTPS 값을 가지며, $proxy_host는 요청을 보낼 업스트림 호스트 값을 갖고, $request_uri는 요청의 세부 경로를 나타낸다.  
즉, 셋을 합친 값은 엑진엑스가 요청을 위임받는 URL이다.  
그 외에도 애플리케이션에 대한 요청을 구분하기 위한 쿼리스트링, 헤더, 세션 식별자 등 여러 요소가 있으며 이 값들을 활용해 직ㅈ버 해시 키를 구성할 수 있다.  

 - 콘텐츠를 어떻게 캐시하고 다시 불러올지 제어하기
    - proxy_cache_key 지시자와 변수를 사용해 캐시 적중과 실패 기준을 정의한다.
    - 엔진엑스가 요청된 페이지를 캐시로 저장할 때 요청 호스트명, URI, 쿠키값으로 사용자마다 서로 다른 해시를 생성해 캐시 키로 사용하도록 한다.
```nginx
proxy_cache_key "$host$request_uri $cookie_user";
```

<br/>

## 캐시 우회

요청한 콘텐츠를 캐시하지 말아야 하는 경우 proxy_cache_bypass 지시자의 매개 변수를 비어 있지 않은 값이나 0이 아닌 값으로 할당하여 요청에 대한 응답을 캐시에서 가져오지 않고 업스트림 서버로부터 받아 전달할 수 있다.  
특정 쿠키와 헤더 값, 쿼리스트링이 존재할 때 캐시 우회를 지정할 수도 있고, 혹은 location 블록과 같이 주어진 콘텍스트 내에서 proxy_cache 지시자를 off로 설정함으로써 캐시 기능을 완전히 끌 수도 있다.  

 - 캐시를 사용하지 않고 우회하기
    - proxy_cache_bypass 지시자를 비어 있지 않은 값이나 0이 아닌 값으로 지정해 캐시를 우회한다. 캐시하고 싶지 않은 location 블록 내에서 지시자의 매개 변수로 사용된 특정 변수 값을 빈 문자열이나 0이 아닌 어떤 값으로든 설정한다.
    - 아래 설정은 cache-bypass라는 HTTP 요청 헤더값이 0이 아닐 때 엔진엑스가 캐시를 우회하도록한다. 캐시를 우회할지 판단하기 위해 특정 헤더값을 변수로 사용하며 사용자는 캐시 우회가 필요하면 이 헤더를 요청에 포함해야 한다.
```nginx
proxy_cache_bypass $http_cache_bypass;
```

<br/>

## 캐시 성능

 - 사용자 환경에 콘텐츠를 캐시해 성능 높이기
    - 사용자 환경에서 유효한 Cache-Control 헤더를 사용한다.
    - 사용자가 CSS와 JS 파일을 캐시하도록 명시한다.
    - expires 지시자는 사용자 환경에 캐시된 콘텐츠가 1년이 지나면 더는 유효하지 않도록 설정한다.
    - add_header 지시자는 HTTP 응답에 Cache-Control 헤더를 추가하며 값을 public으로 지정해 사용자에게 콘텐츠가 전달되는 중간에 위치한 어떤 캐시 서버라도 리소스를 캐시할 수 있도록 한다.
    - 헤더값을 private으로 지정하면 실제 사용자 환경에만 리소스를 캐시한다.
```nginx
location ~* \.(css|js)$ {
    expires 1y;
    add_header Cache-Control "public";
}
```

<br/>

## 캐시 퍼지(엔진엑스 플러스)

엔진엑스 플러스는 캐시된 업스트림 서버의 응답을 무효화하는 간단한 방법을 제공한다.  
proxy_cache_purge 지시자에 0이 아닌 값을 할당하면 조건에 맞는 요청의 캐시를 무효화한다.  

 - 캐시된 콘텐츠를 무효화하기
    - 엔진엑스 플러스의 퍼지 기능을 사용하고 proxy_cache_purge 지시자에 비어있지 않은 값이나 0이 아닌 값을 할당한다.
    - 아래 예제는 HTTP 요청 메서드가 PURGE이면 요청된 리소스에 대한 캐시를 무효화한다.
    - $ curl -XPURGE location/main.js
```nginx
map $request_method $purge_method {
    PURGE 1;
    default 0;
}

server {
    # ..
    location / {
        # ..
        proxy_cache_purge $purge_method;
    }
}
```

<br/>

## 캐시 분할

slice 지시자를 사용하면 엔진엑스가 업스트림 서버의 응답을 1 메가바이트 크기 파일 조각으로 나누고, 나눠진 파일들은 proxy_cache_key 지시자에 지정된 규칙에 따라 저장된다.  
proxy_set_header 지시자를 사용해 원번 서버로 요청을 보낼 때 Range 헤더를 추가하고 헤더값으로 slice_range 변수값을 지정하면, HTTP의 바이트 레인지 요청을 사용할 수 있다. 해당 설정은 HTTP 1.1 버전부터 지원되는 기능으로 proxy_http_version 지시자를 사용해 프로토콜 버전을 업그레이드해야 한다.  

캐시 분할 모듈은 바이트 레인지를 사용하는 HTML5 비디오를 위해 개발되었다.  
바이트 레인지를 사용하면 콘텐츠를 브라우저로 스트리밍과 유사하게 전달할 수 있다.  

 - 용량이 큰 파일을 작은 조각으로 나눠 저장해 캐시 효율 높이기
    - 엔진엑스의 slice 지시자와 내장 변수를 사용해 캐시 결과를 작은 조각으로 나눈다.
```nginx
proxy_cache_path /tmp/mycache keys_zone=mycache:10m;

server {
    # ..
    proxy_cache mycache;
    slice 1m;
    proxy_cache_key $host$uri$is_args$args$slice_range;
    proxy_set_header Range $slice_range;
    proxy_http_version 1.1;
    proxy_cache_valid 200 206 1h;

    location / {
        proxy_pass http://origin:80;
    }
}
```
