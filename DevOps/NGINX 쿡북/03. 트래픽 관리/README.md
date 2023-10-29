# 03장. 트래픽 관리

엔진엑스를 이용해 트래픽 경로를 결정하고 흐름을 제어할 수 있다.  
사용자 요청을 특정 비율로 분기하거나 사용자의 위치 정보를 활용해 흐름을 조절하고 요청 빈도, 연결 수, 대역폭 등을 제한해 트래픽을 제어할 수 있다.  

<br/>

## A/B 테스트

split_clients 모듈을 사용해 사용자 요청을 지정된 비율에 따라 서로 다른 업스트림 풀로 전달한다.  

split_clients 지시자는 첫 번째 매개변수에 지정된 문자열을 활용해 해시를 생성하고, 지정된 비율에 따라 두 번째 매개변수에 지정된 변수에 값을 할당한다.  
split_clients 모듈 공식 문서: https://oreil.ly/Fn61k  

 - split_clients 예시
    - $variant 변수는 요청의 20%에 대해 backendv2가 할당되고, 나머지 80%에 대해 backendv2이 할당된다.
    - 이후 backendv1과 backendv2는 proxy_pass 지시자 등에서 사용할 수 있는 업스트림 서버 풀을 나타낼 수 있다.
        - 수신된 트래픽을 $variant 변수를 사용해 두 개의 애플리케이션 서버 풀로 분기할 수 있다.
```nginx
split_clients "${remote_addr}AAA" $variant {
    20.0%   "backendv2";
    *       "backendv1";
}

server {
    listen 80 _;
    location / {
        proxy_pass http://$variant
    }
}
```

 - 정적 웹사이트 버전 두개로 사용자 분리 처리
```nginx
http {
    split_clients "${remote_addr}" $site_root_folder {
        33.3%       "/var/www/sitev2/";
        *           "/var/www/sitev1/";
    }

    server {
        listen 80 _;
        root $site_root_folder;
        location / {
            index index.html;
        }
    }
}
```

<br/>

## GeoIP 모듈과 데이터베이스 활용

GeoIP 데이터베이스를 설치하고 엔진엑스의 관련 내장 변수를 활성화해 엔진엑스가 로그, 요청 프록시, 요청 분기 등을 수행할 때 사용자 위치를 확인하도록 할 수 있다.  

사용자 위치 확인 기능을 사용하기 위해 엔진엑스 GeoIP 모듈을 설치하고 엔진엑스 서버의 로컬 디스크에 GeoIP 국가 및 도시 데이터베이스를 설치한다.  
geoip_country와 geoip_city 지시자는 GeoIP 모듈에서 사용 가능한 여러 내장 변수를 제공한다.  
geoip_country 지시자는 사용자가 어느 국가에서 접근하는지 식별하는 변수($geoip_country_code, $geoip_country_code3, $geoip_country_name)를 제공한다.  
geoip_city 지시자는 여러 내장 변수($geoip_city_country_code, $geoip_city_country_code3, $geoip_city_country_name, $geoip_city, $geoip_latitude, $geoip_longitude, $geoip_city_continent_code, $geoip_postal_code, $geoip_region, $geo_region_name) 등을 제공한다.  

엔진엑스 geoip 모듈 공식 문서: https://oreil.ly/zleE0  
맥스마인드에서 제공하는 GeoIP 데이터베이스: https://oreil.ly/rJp_a  

 - GeoIP 모듈 설치
```Bash
# 레드햇/센트OS 엔진엑스 오픈 소스 저장소
$ yum install nginx-module-geoip

# 레드햇/센트OS 엔진엑스 플러스 저장소
$ yum install nginx-plus-module-geoip

# 데비안/우분투 엔진엑스 오픈 소스 저장소
$ apt-get install nginx-module-geoip

# 데비안/우분투 엔진엑스 플러스 저장소
$ apt-get install nginx-plus-module-geoip
```

 - GeoIP 국가 및 도시 데이터베이스 다운로드
    - GeoIP 모듈 설치 후 맥스마인드에서 제공하는 GeoIP 국가 및 도시 DB를 다운로드 한다.
    - 공식 사이트: https://dev.maxmind.com/
    - 명령을 순차적으로 실행하면 /etc/nginx/geoip 경로를 생성하고 해당 디렉토리로 이동한 뒤 다운로드한 CSV 형식의 압축된 데이터베이스 파일을 엔진엑스 GeoIP 모듈이 사용할 수 있는 형식으로 변환한다. 엔진엑스의 GeoIP 모듈은 로컬 디스크에 저장된 GeoIP 국가 및 도시 데이터베이스를 이용해 사용자 IP 주소에 대한 위치 정보를 내장 변수로 사용한다.
```Bash
$ mkdir /etc/nginx/geoip
$ cd /etc/nginx/geoip

$ git clone https://githuib.com/sherpya/geolite2legacy.git
$ cd geolite2legacy

$ python3 geolite2legacy.py -i <파일다운로드경로>/GeoLite2-Country-CSV_20220802.zip -f geoname2fips.csv -o GeoIp.dat

$ python3 geolite2legacy.py -i <파일다운로드경로>/GeoLite2-City-CSV_20220802.zip -f geoname2fips.csv -o GeoLiteCity.dat
```

 - 엔진엑스 GeoIP 모듈 설정
    - load_module 지시자는 파일시스템의 지정된 경로에서 모듈을 동적으로 읽어온다.
    - geoip_country 지시자는 IP와 국가 코드 정보가 담긴 파일의 경로를 매개변수로 전달받으며 http 컨텍스트 내에서만 유효하다.
```nginx
load_module "usr/lib64/nginx/modules/ngx_http_geoip_module.so";

http {
    geoip_country /etc/nginx/geoip/GeoIP.dat;
    geoip_city /etc/nginx/geoip/GeoLiteCity.day;
    ..
}
```

<br/>

## 국가 단위 접근 차단하기

 - 비즈니스 요구사항이나 애플리케이션 요건에 따라 특정 국가의 사용자 차단하기
    - map 지시자를 사용해 접근을 차단하거나 허용할 국가 코드를 변수에 할당한다.
    - map 지시자는 $country_access 변수에 1이나 0을 할당한다. 사용자 IP 주소의 위치 정보가 미국(US)이면 변수에 0을 할당하고, 그 외에는 기본값인 1을 할당한다.
```nginx
server {
    if ($country_access = '1') { # 미국이 아닌 국가는 403 반환
        return 403;
    }
    ..
}
```

<br/>

## 실제 사용자 IP 찾기

엔진엑스 앞단에 프록시 서버를 운용한다면 엔진엑스가 식별하는 사용자 IP는 실제 사용자가 아닌 프록시 서버의 IP이다.  
geoip_proxy 지시자를 사용해 특정 IP 대역에서 들어오는 요청에 대해 X-Forwarded-For 헤더값을 참조하도록 할 수 있다.  
geoip_proxy 지시자는 단일 IP 주소나 CIDR 표기법을 사용한 IP 주소 대역을 사용하며, 요청이 여러 프록시를 경유해 들어오면 geoip_proxy_recursive 지시자를 사용해 X-Forwarded-For 헤더에 기록된 각 프록시 주소를 탐색해 실제 사용자 IP를 찾을 수 있다.  

엔진엑스 앞단에 AWS 일래스틱 로드 밸런서(AWS ELB)나 구글 클라우드 플랫폼(GCP)의 로드 밸런서 또는 마이크로소프트 애저의 로드 밸런서를 사용할 때 이러한 방식으로 실제 사용자 IP를 확인한다.  

 - 사용자 요청이 프록시 서버를 경유해 엔진엑스 서버에 전달됐을 대 실제 사용자 IP 확인하기
    - geoip_proxy 지시자로 프록시 서버 IP 대역을 정의하고 geoip_proxy_recursive 지시자로 사용자의 원래 IP 주소를 확인한다.
    - geoip_proxy 지시자에 CIDR 표기법으로 프록시 서버의 IP 대역을 지정하고, 엔진엑스가 X-Forwarded-For 헤더값을 활용해 실제 사용자 IP를 찾도록 한다.
    - geoip_proxy_recursive 지시자를 사용하면 엔진엑스는 X-Forwarded-For 헤더값을 순차적으로 탐색해 최종 사용자의 IP를 확인한다.
```nginx
load_module "/usr/lib64/nginx/modules/ngx_http_geoip_module.so";

http {
    geoip_country /etc/nginx/geoip/GeoIP.dat;
    geoip_city /etc/nginx/geoip/GeoLiteCity.dat;
    geoip_proxy 10.0.16.0/26;
    geoip_proxy_recursive on;
    ..
}
```

<br/>

## 연결 제한하기

 - 사용자 IP 주소와 같이 사전에 정의된 키값에 따라 연결 수 제한하기
    - 연결에 대한 지표를 저장할 공유 메모리 영역을 만들고 limit_conn 지시자를 사용해 연결 수를 제한한다.
    - 아래 설정은 limitbyaddr 이라는 공유 메모리 영역을 생성한다. 사전에 정의된 키는 바이너리 형태로 변환된 사용자의 IP 주소이다. 공유 메모리 영역의 크기는 10 메가바이트로 설정한다.
        - limit_conn 지시자는 limit_conn_zone 지시자로 선언한 공간 이름과 허용 연결 수를 매개변수로 받는다.
        - limit_conn_status 지시자는 지정된 연결 수를 초과하면 사용자에게 전달할 HTTP 상태 코드를 지정한다. (HTTP 429: 요청이 너무 많음)
        - limit_conn과 limit_conn_status 지시자는 http, server, location 컨텍스트에서 사용할 수 있다.
```nginx
http {
    limit_conn_zone $binary_remote_addr zone=limitbyaddr:10m;
    limit_conn_status 429;
    # ..
    server {
        # ..
        limit_conn limitbyaddr 40;
        # ..
    }
}
```

<br/>

## 요청 빈도 제한하기

빈도 제한 모듈을 사용해 일반 사용자에게는 정상적인 서비스를 제공하면서 악의적으로 아주 많은 요청을 보내는 사용자의 접근을 제한할 수 있다.  
로그인 페이지에 강력한 요청 빈도 제한을 적용해 브루트포스 공격을 차단하거나, 매우 엄격한 요청 빈도 제한으로 악의적인 사용자가 애플리케이션을 응답 불능 상태에 빠뜨리거나 서버 리소스를 고갈시키는 문제에 대응한다.  


 - 사용자 IP 주소와 같이 사전에 정의된 키값을 이용해 요청 빈도 제한하기
    - 빈도 제한 모듈을 활용해 요청 빈도를 제한한다.
    - limitbyaddr 이라는 이름으로 공유 메모리 영역을 생성하고, 사용자 IP 주소를 바이너리 형태로 변환해 사전에 정의된 키로 활용한다. 영역의 크기는 10 메가바이트로 지정한다.
        - limit_req 지시자는 zone 매개변수를 통해 키를 전달받는다. zone 매개변수는 어떤 공유 메묄 영역을 참고해 요청 빈도를 제한할지 결정한다.
        - limit_req_status 지시자로 지정된 빈도를 초과하는 요청에 대해 429 응답 코드를 반환할 수 있다. 해당 지시자로 별도의 응답 코드를 지정하지 않으면 기본적으로 403이 반환된다.
```nginx
http {
    limit_req_zone $binary_remote_addr zone=limitbyaddr:10m rate=3r/s;
    limit_req_status 429;
    #..
    server {
        # ..
        limit_req zone=limitbyaddr;
        # ..
    }
}
```

 - limit_req 두 단계 요청 빈도 제한
    - 사용자 측에서 한 번에 많은 요청을 전송한 후 일정 시간 동안 빈도를 줄이는 경우 burst 매개변수를 사용해 빈도가 지정된 값보다 낮으면 차단하지 않고 허용하도록 설정할 수 있다.
    - delay 값을 초과한 요청은 지정된 rate에 맞춰 지연 처리한다.
```
server {
    location / {
        limit_req zone=limitbyaddr burst=12 delay=9;
    }
}
```

<br/>

## 전송 대역폭 제한하기

대역폭을 제한하는 데는 limit_rate_after와 limit_rate 지시자를 사용한다.  
두 지시자는 모두 http, server, location 컨텍스트와 lo-cation 블록 내부에 위치한 if 문 등 다양한 곳에서 사용할 수 있다.  

limit_rate_after 지시자는 특정 연결에서 지정된 양만큼 데이터가 전송되지 않았으면 대역폭이 제한되지 않도록 한다.  
limit_rate 지시자는 초당 전송량을 매개변수로 사용하며, 사용된 모듈과 블록에 따라 지정된 수치에 맞춰 대역폭을 제안한다.  


 - 서비스 리소스의 부하를 막기 위해 사용자당 다운로드 대역폭을 제한하기
    - limit_rate와 limit_rate_after 지시자를 사용해 사용자에 대한 응답 대역폭을 제한한다.
    - /download/ 경로로 시작하는 URI에 대해 누적 전송량이 10메가바이트를 초과하면 초당 1메가바이트를 넘지 않도록 제한한다.
    - 대역폭 제한은 개별 연결에 적용되는 설정이므로 연결 수와 함께 전송 대역폭을 제한할 필요가 있다.
```nginx
location /download/ {
    limit_rate_after 10m;
    limit_rate 1m;
}
```
