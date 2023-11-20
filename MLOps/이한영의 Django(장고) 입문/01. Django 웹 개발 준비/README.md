# Django 웹 개발 준비

Django는 파이썬으로 작성된 오픈 소스 웹 프레임워크로, 웹 애플리케이션을 빠르게 개발하고 유지보수하는 데 도움을 주는 도구와 기능을 제공합니다.  
Django는 모델-뷰-컨트롤러 (MVC) 아키텍처 패턴을 기반으로 한 MTV(Model-Template-View) 아키텍처를 사용하며, 이는 소프트웨어를 데이터 모델, 사용자 인터페이스 및 비즈니스 로직으로 구분하는 방식입니다.  

 - ORM (Object-Relational Mapping): Django는 데이터베이스와의 상호 작용을 쉽게 만들어주는 ORM을 제공합니다. 이를 통해 개발자는 SQL 쿼리 대신 파이썬 코드를 사용하여 데이터베이스와 상호 작용할 수 있습니다.
 - Admin 패널: Django는 자동으로 생성되는 관리자 인터페이스를 제공하여 데이터베이스 관리를 쉽게 할 수 있습니다. 이를 통해 데이터를 추가, 수정, 삭제할 수 있고, 사용자 인증 및 권한 관리를 손쉽게 구현할 수 있습니다.
 - URL 패턴 매칭: URL 패턴 매칭을 통해 URL을 뷰 함수와 매핑시켜주어 간편한 URL 관리를 가능하게 합니다.
 - 템플릿 엔진: Django는 강력한 템플릿 엔진을 내장하고 있어, 동적으로 생성된 HTML 페이지를 쉽게 만들 수 있습니다.
 - 보안 기능: Django는 기본적으로 보안 기능을 많이 포함하고 있습니다. 예를 들면, CSRF(Cross-Site Request Forgery) 및 XSS(Cross-Site Scripting)와 같은 보안 취약점으로부터 애플리케이션을 보호합니다.
 - 풍부한 확장성: Django는 다양한 애플리케이션을 쉽게 통합할 수 있는 유연한 확장성을 제공합니다.
 - 커뮤니티 및 문서: Django는 활발한 개발자 커뮤니티와 풍부한 문서를 가지고 있어, 개발자들은 도움을 받기 쉽습니다.

<br/>

## Django 다양한 내장 기능과 파이썬 확장 기능

 - 데이터베이스 관리
 - 이메일 전송
 - 언어별 번역 관리
 - 로그인/회원가입/비밀번호 변경 등의 인증
 - RSS 피드/검색 엔진을 위한 Sitemap 생성
 - CSV, PDF 생성 기능
 - Django 확장 프로그램
    - 문자 메시지 보내기
    - 채팅
    - 온라인 결제
    - WYSIWYG 에디터
    - 모바일 앱(안드로이드, iOS)에 푸시 메시지 발송

<br/>

## 개발환경 구성

 - Python: https://python.org/downloads
 - PyCharm: https://www.jetbrains.com/pycharm/download/
```
1. 파이참 프로젝트 생성
 - PyCharm > New Project
    - Location: 사용할 프로젝트 폴더 지정
    - New environment using: Virtualenv
        - Location: 프로젝트 폴더/venv
        - Base interpreter: 설치한 Python 버전
    - Create a main.py welcome script: 체크해제

2. 가상 환경 생성
$ python -m venv venv
```

 - `가상 환경 활성화`
```Bash
# 가상 환경 활성화
$ .\venv\Scripts\active

# 가상 환경 비활성화
$ .\venv\Scripts\deactivate.bat

# 권한 에러 발생시: Windows PowerShell 관리자로 실행
$ Set-ExecutionPolicy RemoteSigned
$ Y

# 패키지 설치
$ pip install 패키지명
```
