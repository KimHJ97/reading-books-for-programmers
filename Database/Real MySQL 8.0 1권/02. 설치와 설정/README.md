# 설치와 설정

## 버전과 에디션 선택

초기 버전의 MySQL 서버는 엔터프라이즈 에디션과 커뮤니티 에디션으로 나뉘어 있기는 했지만 실제 MySQL 서버의 기능적 차이는 없고, 기술 지원의 차이만 있었다. 하지만, MySQL 5.5 버전부터는 커뮤니티와 엔터프라이즈 에디션의 기능이 달라지면서 소스코드도 달라졌고, MySQL 엔터프라이즈 에디션의 소스코드는 더이상 공개되지 않는다.  

하지만, MySQL 서버의 상용화 전략의 핵심 내용은 엔터프라이즈 에디션과 커뮤니티 에디션 모두 동일하며, 특정 부가 기능들만 상용 버전인 엔터프라이즈 에디션에 포함되는 방식이다. (오픈 코어 모델) 즉, MySQL 엔터프라이즈 에디션과 커뮤니티 에디션의 핵심 기능은 거의 차이가 없다.  
 - 엔터프라이즈 에디션 지원 기능
    - Thread Pool
    - Enterprise Audit
    - Enterprise TDE
    - Enterprise Authentication
    - Enterprise Firewall
    - Enterprise Monitor
    - Enterprise Backup
    - MySQL 기술 지원

<br/>

## MySQL 설치

 - `리눅스 환경(Yum)`
    - Yum 인스톨러를 이용하려면 MySQL 소프트웨어 레포지토리를 등록해야 하는데, 이를 위해서는 MySQL 다운로드페이지에서 RPM 설치 파일을 직접 받아서 설치해야 한다.
    - 운영체제 버전에 맞는 RPM 파일을 다운로드해서 MySQL 서버를 설치하고자 하는 리눅스 서버에서 Yum 레포지토리 정보를 등록한다.
```bash
# Yum 레포지토리 정보 등록
$ sudo rpm -Uvh mysql80-community-release-el7-3.noarch.rpm

# MySQL 설치용 RPM 파일 확인
$ ls -alh /etc/yum.repos.d/*mysql*

# 설치 가능한 MySQL 소프트웨어 목록 확인
$ sudo yum search mysql-community

# 설치 가능한 모든 버전 확인
$ sudo yum --showduplicates list mysql-community-server

# MySQL 8.0.20 버전 설치
$ sudo yum install mysql-community-server-8.0.21
```

<br/>

 - `리눅스 환경(RPM)`
    - Yum 인스톨러를 사용하지 않고 RPM 패키지로 직접 설치하려면 설치에 필요한 RPM 패키지 파일들을 직접 다운로드해야 한다.
    - RPM 패키지 다운로드 페이지에서 RPM 패키지 파일들을 다운로드한 후 의존 관계 순서대로 설치한다.
        - Development Libraries
        - Shared Libraies
        - Compatibility Libraies
        - MySQL cONFIGURATION
        - MySQL Server
        - Client Utilities
```bash
$ rpm -Uvh mysql-community-devel-8.0.21-1.el7.x86_64.rpm
$ rpm -Uvh mysql-community-libs-8.0.21-1.el7.x86_64.rpm
$ rpm -Uvh mysql-community-libs-compat-8.0.21-1.el7.x86_64.rpm
$ rpm -Uvh mysql-community-common-8.0.21-1.el7.x86_64.rpm
$ rpm -Uvh mysql-community-server-8.0.21-1.el7.x86_64.rpm
$ rpm -Uvh mysql-community-client-8.0.21-1.el7.x86_64.rpm
```

<br/>

 - `macOS용 DMS 패키지 설치`
    - MacOS에서 인스톨러로 설치하려면 설치에 필요한 DMG 패키지 파일들을 직접 다운로드해야 한다.
    - MySQL 서버가 설치된 디렉토리는 '/usr/local/mysql'이다.
        - bin: MySQL 서버와 클라이언트 프로그램, 유틸리티를 위한 디렉토리
        - data: 로그 파일과 데이터 파일들이 저장되는 디렉토리
        - include: C/C++ 헤더 파일들이 저장되는 디렉토리
        - lib: 라이브러리 파일들이 저장된 디렉토리
        - share: 다양한 지원 파일들이 저장돼 있으며, 에러 메시지나 샘플 설정 파일(my.cnf)이 있는 디렉토리
```bash
# MySQL 설치 디렉토리 확인
$ ps -ef | grep mysqld

# MySQL 서버 시작
$ sudo /usr/local/mysql/support-files/mysql.server start

# MySQL 서버 종료
$ sudo /usr/local/mysql/support-files/mysql.server stop
```

<br/>

 - `윈도우 MSI 인스톨러 설치`
    - 윈도우에서 인스톨러로 MySQL 서버를 설치하려면 설치에 필요한 윈도우 인스톨 프로그램을 직접 다운로드해야 한다.
```
1. Choosing a Setup Type
 - 설치 유형 선택 화면
    - Developer Default: MySQL 서버와 클라이언트 도구, MySQL Workbech 같은 GUI 클라이언트 도구 모두 설치
    - Custom: 필요한 소프트웨어만 선택

2. Select Products and Features
 - 설치할 소프트웨어 직접 선택
    - 꼭 필요한 소프트웨어인 MySQL 서버와 MySQL Sheel, MySQL Router 선택
 - High Availability
    - 고가용성 옵션 선택
    - Standalone MySQL Server: 복제 없이 단일 서버 실행 모드
 - Type and Networking
    - MySQL 서버를 어떤 방식으로 접속하게 할지 설정
    - Config Type: Development Computer
    - TCP/IP, Port:3306, X Protocol Port: 33060
 - Authentication Method
    - 사용자 로그인 시점에 사용할 비밀번호 인증 방식
    - Strong Password Encryption: Caching SHA-2 Authentication 플러그인 사용
    - Legacy Authentication Method: Native Authentication 플러그인 사용 (테스트용 으로 해당 선택)
 - Accounts and Roles
    - MySQL 서버의 관리자 계정(root 계정)의 비밀번호 입력

3. MySQL 설정 완료 후
MySQL 서버의 프로그램과 설정 파일(my.ini)의 위치는 윈도우 서비스 화면에서 'MySQL80' 서비스의 등록 정보를 통해 확인 가능
 - MySQL Server: C:/Program Files/MySQL/MySQL Server 8.0
 - MySQL Shell: C:/Program Files/MySQL/MySQL Shell 8.0
 - MySQL Router: C:/Program Files/MySQL/MySQL Router 8.0
```
