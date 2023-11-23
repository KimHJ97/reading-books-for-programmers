# 사이트를 온라인에 올리기

## AWS Lightsail

Amazon Lightsail은 Amazon Web Services (AWS)에서 제공하는 간편한 웹 서비스입니다. Lightsail은 개발자, 기업 소유자 및 다른 사용자들이 웹 사이트, 웹 응용 프로그램 및 기타 애플리케이션을 쉽게 배포, 관리 및 확장할 수 있도록 하는 서비스입니다. Lightsail은 사용자 친화적인 인터페이스를 통해 서버, 네트워크 및 데이터베이스 리소스에 쉽게 액세스할 수 있도록 설계되어 있습니다.  

Lightsail은 사전 구성된 애플리케이션 스택을 제공하며, 사용자는 몇 분 만에 웹 사이트 또는 애플리케이션을 배포할 수 있습니다. 또한, Lightsail은 서버 인스턴스, 스토리지, 네트워크 및 데이터베이스에 대한 간단한 월간 요금 체계를 제공하여 예측 가능하고 투명한 비용을 제공합니다.  

Lightsail은 기본적인 웹 호스팅에서부터 더 복잡한 웹 애플리케이션까지 다양한 용도에 사용될 수 있습니다. 이 서비스는 AWS의 강력한 기능을 활용하면서도 사용자가 복잡한 구성 작업을 최소화할 수 있도록 고안되었습니다.  

<br/>

### Lightsail과 EC2

Amazon EC2 (Elastic Compute Cloud)와 Amazon Lightsail은 모두 Amazon Web Services (AWS)에서 제공하는 클라우드 컴퓨팅 서비스입니다. 그러나 두 서비스 간에는 몇 가지 중요한 차이점이 있습니다.  
간단하고 예측 가능한 프로젝트를 위해서는 Lightsail이 적합할 수 있고, 더 복잡하고 유연한 구성이 필요한 경우 EC2를 선택할 수 있습니다.  

 - 복잡성과 유연성:
    - EC2: EC2는 매우 유연하며 복잡한 구성이 가능한 서비스입니다. 사용자는 가상 머신의 운영 체제, 인스턴스 유형, 스토리지, 네트워크 구성 등을 선택하고 조정할 수 있습니다.
    - Lightsail: Lightsail은 더 단순하고 사용자 친화적인 서비스로, 사전 구성된 템플릿과 통합 관리 인터페이스를 제공하여 초보자나 간단한 애플리케이션을 위한 것입니다.
 - 가격 모델:
    - EC2: EC2는 사용한 컴퓨팅 리소스에 따라 지불해야 하는 온디맨드 및 예약 인스턴스와 같은 다양한 가격 모델을 제공합니다.
    - Lightsail: Lightsail은 간단한 월간 요금 체계를 사용하며, 미리 지정된 서버 인스턴스, 스토리지 및 네트워크에 대한 통합된 가격을 제공합니다. 이것은 예측 가능하고 투명한 비용을 제공합니다.
 - 관리 및 운영 간소화:
    - EC2: EC2에서는 모든 측면을 직접 구성하고 관리해야 합니다. 운영 체제 업데이트, 보안 패치, 확장 등에 대한 모든 책임이 사용자에게 있습니다.
    - Lightsail: Lightsail은 통합된 관리 콘솔을 통해 사용자가 필요로 하는 대부분의 작업을 단순화하고 자동화합니다. 이는 초보자가 빠르게 시작할 수 있도록 도움을 줍니다.
 - 용도:
    - EC2: EC2는 대규모 및 복잡한 워크로드, 자체 설계된 환경 또는 특별한 요구 사항을 가진 애플리케이션에 적합합니다.
    - Lightsail: Lightsail은 간단한 웹 사이트, 블로그, 소규모 애플리케이션, 개인 프로젝트 및 초보자를 대상으로 하는 작은 및 중간 규모의 프로젝트에 적합합니다.

<br/>

### Lightsail 사용하기

 - `인스턴스 생성`
```
1. Lightsail 콘솔로 이동
 - https://lightsail.aws.amazon.com

2. 인스턴스 생성
 - Create instance 클릭
    - 인스턴스 이미지 선택
        - Linux/Unix -> Ubuntu 20.04 LTS
    - 인스턴스 플랜 선택
        - 가장 낮은 성능의 Plan을 선택하면, 월 3.5달러가 청구된다.

3. 인스턴스에 접속하기
 - Connect using SSH 버튼 클릭
```

<br/>

 - `인스턴스 접속 테스트`
    - Lightsail로 생성한 인스턴스는 브라우저로부터 오는 요청을 받을 수 있다.
    - 요청을 처리할 Django 서버를 구축하기 전에, 파이썬에 내장된 HTTP 서버를 사용해 요청을 테스트한다.
        - 파이썬 내장 HTTP 서버는 서버를 실행한 위치에 index.html 파일이 있다면 해당 내용을 보여주고, 없다면 파일 목록을 보여준다.
    - Lightsail 인스턴스 상세 화면에서 Networking 탭에서 공인 IP를 확인할 수 있다.
```Bash
# HTTP 서버 실행
$ sudo python3 -m http.server 80

# index.html 파일 만들기
$ echo '<h1>Hello Django!</h1>' > index.html
$ sudo python3 -m http.server 80
```

<br/>

 - `인스턴스 설정`
    - __고정 IP 설정__
        - IP 주소는 설계의 한계로 인터넷상에 42억 개 가량만 생성할 수 있는 한정된 자원이다. 떄문에, AWS 사용 중 인스턴스에 할당된 IP는 특정 시점에 변경되거나 삭제될 수 있다.
        - Lightsail의 비용은 기본적으로 고정IP 주소를 서비스로 제공한다.
        - Lightsail 콘솔 > 인스턴스 상세 > Networking탭 > PUBLIC IP > Attach static IP > Create and attach a static IP
    - __SSH KEY 사용__
        - Connect using SSH 버튼을 눌러 웹으로 터미널을 사용할 수도 있지만, SSH Key를 사용해 내 컴퓨터의 터미널을 사용해 접속할 수도 있다.
        - SSH Key 다운로드 후 해당 Key로 터미널에 접속한다.
    - __소스코드 전송__
        - scp 명령어로 터미널에서 다른 컴퓨터 간 파일을 전송할 수 있다.
        - scp 명령어 사용시 기존에 있던 파일은 덮어씌워지지만, 삭제된 파일은 전송된 곳에서 자동 삭제되지는 않는다.
        - 때문에, 로컬에서 소스코드가 변경되었다면 서버에 코드를 삭제하고 로컬에 소스코드를 재전송해준다.
```Bash
# SSH Key의 이름은 django-key.pem으로 한다.
$ chmod 400 ~/django-key.pem

# SSH Key로 서버 접속
$ ssh -i ~/django-key.pem ubuntu@{AWS IP}
yes

# 서버에 소스코드 전송 (scp 명령어)
# 서버 보안 접근은 SSH Key(django-key.pem)을 사용하고, pystagram 디렉토리를 서버의 /home/ubuntu로 복사한다.
$ scp -i ~/django-key.pem -r pystagram ubuntu@{AWS IP}:/home/ubuntu/
```

<br/>

## Django 실행

 - `배포를 위한 구조 변경`
    - __소스 코드가 아닌 파일__
        - Django는 기본적으로 SQLite3을 내장하고 있다.
        - 만약, 개발환경에서 사용하고 해당 내용을 그대로 올린다면 개발 환경에 데이터들이 포함되어 운영 서버에 전송되게 된다.
        - 그외에도, venv 디렉토리는 소스코드가 아니고, 서버에서 사용되지 않는다. 때문에, 이 용량이 큰 폴더를 업로드하는 것은 비효율적이기 때문에 해당 폴더도 변경해주어야 한다.
    - __venv 위치 변경__
        - 가상환경 디렉토리를 옮길 때는 PyCharm에서 추가적인 설정이 필요하다.
        - 우측 하단 > Add New Interpreter > Add Local Interpreter..
            - Environment: New
            - Location: 상위 폴더에 위치하도록 경로 지정
        - 이후 기존 가상 환경 디렉토리 삭제 후 기존 라이브러리 재설치
            - pip install 'django<5' 'pillow<10' 'django-admin-thumbnails<0.3'
```
# 변경전
pystagram
 ├── [소스코드]
 ├── media/      # 사용자가 업로드한 파일
 ├── db.sqlite3  # 데이터베이스 파일
 └── venv/       # 가상환경 디렉토리

# 변경후
~/PycharmProjects/
 ├── media/          # 사용자가 업로드한 파일
 ├── db.sqlite3      # 데이터베이스 파일
 ├── pystagram-venv/ # 가상환경 디렉토리
 └── pystagram
      └─ [소스코드]
```
```py
# settings.py: 데이터베이스 파일 및 미디어 파일 위치 변경
# 위치를 지정해주고, python manage.py migrate를 실행하면 새로운 위치에 데이터베이스 파일이 생성된다.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent / "pystragram-db.sqlite3" # 상위 디렉토리로 설정
    }
}

MEDIA_ROOT = BASE_DIR.parent / "pystragram-media"

```

<br/>

 - `파이썬 패키지 추출`
    - 개발환경에 설치된 파이썬 패키지들을 서버에도 설치해야 한다.
```Bash
# 현재 설치된 패키지 목록 확인
$ pip list

# 현재 설치된 패키지 목록을 텍스트 파일로 추출
$ pip freeze > requirements.txt

# 추출된 텍스트 파일 확인
$ cat requirements.txt
```

<br/>

 - `서버에 패키지 설치`
    - 위에서 만든 requirements.txt 파일로 서버에 같은 패키지를 설치한다.
    - 로컬에서 pip install로 새 패키지를 설치할 때마다 pip freeze를 사용해 requirements.txt를 생성하고, 서버에서는 scp로 소스코드와 함께 requirements.txt 파일을 받아 로컬에 설치한 것과 같은 버전의 패키지들을 설치해주어야 한다.
```Bash
# 서버에 있는 소스코드 삭제
$ ssh -i ~/django-key.pem ubuntu@{AWS IP} rm -r /home/ubuntu/pystagram

# 로컬 소스코드를 서버에 업로드
$ scp -i ~/django-key.pem -r pystagram ubuntu@{AWS IP}:/home/ubuntu

# 파이썬 패키지 설치
# 1. 터미널로 서버 접속 후 프로젝트 디렉토리로 이동
$ ssh -i ~/django-key.pem ubuntu@{AWS IP}
$ sudo su
$ cd /home/ubuntu/pystagram

# 2. pip를 설치하지 않은 경우 설치
$ apt update
$ apt install python3-pip
Y

# 3. requirements.txt 파일을 사용해 패키지 설치
$ pip install -r requirements.txt

```

<br/>

 - `서버 실행`
    - runserver는 기본적으로 127.0.0.1이라는 IP 주소로 실행된다.
    - 해당 주소는 루프백 주소로 로컬 환경에서 접근할 때 문제가 없었지만, 서버에서 실행한 runserver를 외부에서 접근할 수 없다.
    - 때문에, 127.0.0.1 대신 0.0.0.0으로 서버가 실행되도록 한다. (Lightsail 서버는 기본적으로 80 포트가 열려있다.)
    - __Django 설정 파일 수정__
        - Django는 기본적으로 지정하지 않은 도메인이나 IP 주소로부터의 접속을 차단한다.
        - 때문에, config/settings.py에 다른 IP 주소와 도메인을 허용하도록 설정한다.
        - ALLOWED_HOSTS = ["*"]
```Bash
# runserver 실행
$ python3 manage.py migrate
$ python3 manage.py runserver

# 외부에서 접근 가능하도록 runserver 실행
$ python3 manage.py runserver 0.0.0.0:80
$ python3 manage.py runserver 0:80 # 0.0.0.0:80은 0:80으로 줄여서 쓸 수 있다.

# 백그라운드로 runserver 실행
$ nohup python3 manage.py runserver 0:80 &

# 백그라운드 runserver 종료
$ ps -ax | grep runserver
$ pkill -9 python3
```
