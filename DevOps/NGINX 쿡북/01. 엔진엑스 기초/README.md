# 01장. 엔진엑스 기초

## 엔진엑스 설치

 - 데비안/우분투 리눅스 배포판
    - 운영체제의 패키지 정보를 업데이트하고 엔진엑스 공식 패키지 저장소 설정을 도와줄 몇 가지 패키지를 설치한다.
```Bash
apt-get update
apt install -y curl gnupg2 ca-certificates lsb-release debian-archive-keyring

# 엔진엑스 패키지 저장소와 서명키 다운로드 후 저장
curl https://nginx.org/keys/nginx_signing.key | gpg --dearmor | sudo tee /usr/share/keyrings/nginx-archive-keyring.gpg >/dev/null

# lsb_release 명령을 이용해 운영체제와 배포판 이름을 정의하는 변수를 선언하고 apt 소스 파일 생성
OS=$(lsb_release -is | tr '[:upper:]' '[:lower:]')
RELEASE=$(lsb_release -cs)
echo "deb [signed-by=/usr/share/keyrings/nginx-archive-keyring.gpg] \
    http://nginx.org/packages/${OS} ${RELEASE} nginx" \
    | sudo tee /etc/apt/sources.list.d/nginx.list

# 패키지 정보를 한 번더 업데이트하고 엔진엑스 설치
apt-get update
apt-get install -y nginx
nginx
```

<br/>

 - 레드햇/센트OS 리눅스 배포판
    - nginx.repo 파일은 레드햇 계열 리눅스 배포판의 패키지 관리자인 YUM이 엔진엑스의 공식 패키지 저장소를 활용하도록 한다.
    - yum 명령으로 오픈 소스 엔진엑스를 공식 패키지 저장소로 다운로드받고, systemctl 명령으로 엔진엑스가 시스템 부팅시 systemd를 통해 활성화되고 자동으로 시작되도록 한다.
    - firewall-cmd 명령으로 HTTP의 기본 80 포트로 들어오는 TCP 프로토콜 요청을 엔진엑스가 수신하도록 한다.
    - 마지막으로 변경된 방화벽 정책이 적용되도록 방화벽 리로드한다.
```Bash
# /etc/yum.repos.d/nginx.repo 파일
[nginx]
name=nginx repo
baseurl=http://nginx.org/packages/OS/OSRELEASE/$basearch/
gpgcheck=0
enabled=1

# 명령 수행
yum -y install nginx
systemctl enable nginx
systemctl start nginx
firewall-cmd --permanent --zone=public --add-port=80/tcp
firewall-cmd --reload
```

<br/>

 - 설치 상태 점검하기
```Bash
$ nginx -v
$ ps -ef | grep nginx
```

<br/>

## 엔진엑스 주요 설정 파일, 디렉토리, 명령어

### 주요 설정 파일과 디렉토리

 - etc/nginx/
    - 엔진엑스 서버가 사용하는 기본 설정이 저장된 루트 디렉토리
 - /etc/nginx/nginx.conf
    - 엔진엑스의 기본 설정 파일로, 모든 설정에 대한 진입점
    - 워커 프로세스 개수, 튜닝, 동적 모듈 적재와 같은 글로벌 설정 항목을 포함하며, 다른 엔진엑스 세부 설정 파일에 대한 참조를 지정한다.
 - /etc/nginx/conf.d/
    - 기본 HTTP 서버 설정 파일을 포함하는 디렉토리
    - 엔진엑스 설정은 include 구문을 활용해 구조화함으로써 각 설정 파일을 간결하게 유지할 수 있다.
    - 몇몇 패키지 저장소에서 배포되는 엔진엑스는 설치 시 conf.d 디렉토리 대신에 site-enabled 디렉토리가 있고, symlink를 통해 site-available 디렉토리에 저장된 설정 파일들이 연결되는 경우도 있다. (해당 방식은 더이상 사용 X)
 - /var/log/nginx/
    - 엔진엑스의 로그가 저장되는 디렉토리
    - access.log와 error.log 파일이 존재하며, 접근 로그 파일은 엔진엑스 서버가 수신한 개별 요청에 대한 로그를 저장하며, 오류 로그 파일은 오류 발생 시 이벤트 내용을 저장한다.

<br/>

### 엔진엑스 기초 명령어

 - nginx -h: 도움말
 - nginx -v: 버전 정보
 - nginx -V: 버전 정보 + 빌드 정보
 - nginx -t: 설정 테스트
 - nginx -T: 설정 테스트 및 결과 출력
 - nginx -s signal: 신호를 엔진엑스 마스터 프로세스에 전송 (stop, quit, reload, reopen)
    - stop: 엔진엑스 프로세스 즉시 종료
    - quit: 현재 진행 중인 요청을 모두 처리한 뒤 엔진엑스 프로세스 종료 (graceful shutdown)
    - reload: 엔진엑스가 설정을 다시 읽어들임 (무중단으로 설정 리로드)
    - reopen: 지정된 로그 파일을 다시 열도록 명령

<br/>

## 정적 콘텐츠 서비스하기

 - /etc/nginx/conf.d/default.conf
    - HTTP 프로토콜과 80 포트를 이용해 /usr/share/nginx/html/ 경로에 저장된 정적 콘텐츠를 제공한다.
    - server 블록: 엔진엑스가 처리할 새로운 컨텍스트 정의
    - 만약, 설정에 default_server 매개변수를 통해 기본 컨텍스트로 지정되지 않으면, 엔진엑스는 요청 호스트 헤더값이 server_name 지시자에 지정된 값과 같을 때만 server 블록에 지정된 내용을 수행한다. 즉, 서버가 사용할 도메인이 정해지지 않았다면 default_server 매개변수를 사용해 기본 컨텍스트를 정의하고 server_name 지시자를 생략할 수 있다.
```nginx
server {
    listen 80 default_server;     # 80 포트 요청 수신
    server_name www.example.com;  # 서버가 처리할 호스트, 도메인명

    location / {
        root /usr/share/nginx/html;
        # alias /usr/share/nginx/html;
        index index.html index.htm;
    }
}
```
