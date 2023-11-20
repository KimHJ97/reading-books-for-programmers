# 02장. pyburger 프로젝트

## Django의 디자인 패턴

### `MTV 패턴`

MTV 패턴은 모델-템플릿-뷰(Model-Template-View) 디자인 패턴으로 역할에 ㄸ라ㅏ 코드를 분리하는 가이드로 사용한다.  

 - Model: 모델(Model)은 Django와 데이터베이스를 연결시켜주는 코드이며 데이터의 형태를 나타낸다. 일반적으로 각각의 모델은 데이터베이스 테이블과 매핑된다.
 - Template: 템플릿(Template)은 웹 브라우저로 돌려줄 코드이며, 사용자에게 제공될 결과물의 형태를 나타낸다. HTML을 사용해서 ㅏ타내며, Django에서는 templates 디렉토리 내에 HTML 파일을 사용한다.
 - View: View는 사용자의 요청을 받아 처리하는 웹 사이트의 로직을 가지는 코드이다. 파이썬의 함수를 사용한다.
 - Tips: Django의 MTV 패턴은 유명한 소프트웨어 디자인 패턴인 모델-뷰-컨트롤러(Model-View-Controller, MVC)와 같은 패턴이며, 부르는 명칭에만 차이가 있다.
    - MVC의 View = MTV의 Template
    - MVC의 Controller = MTV의 View
    - 장고가 MTV를 사용하는 이유: https://docs.django.ac/mtv

<br/>

## Django 설치와 프로젝트 생성

 - `Django 설치`
```Bash
# 4 버전 설치
(venv) pip install 'django<5'

# 버전 확인
(venv) django-admin --version
```

<br/>

 - `Django 프로젝트 생성`
    - 터미널에서 django-admin 명령어로 장고 프로젝트를 만들 수 있다.
    - startproject 명령어로 프로젝트 기반 구조를 만들 수 있다.
```Bash
# 현재 경로의 장고 프로젝트 생성
(venv) django-admin startproject config .

# 장고 프로젝트 실행
(venv) python manager.py runserver
```

<br/>

 - `루프백 주소로의 요청`
    - 장고 프로젝트를 만들고 실행하면 기본적으로 127.0.0.1:8000 으로 실행된다.
    - 루프백(Loopback, loop-back)은 신호가 원래의 장치로 돌아가는 것을 말하며, 주로 전송을 테스트하는 데 사용한다. 네트워크에서 "localhost" 또는 "127.0.0.1"이 루프백 주소로 사용되며, 이 주소로 요청을 전송하면 요청은 전송한 컴퓨터로 돌아오게 된다.
```
 - 외부 네트워크(인터넷)로의 요청
브라우저의 URL을 입력하여 요청하면 컴퓨터 외부의 네트워크(인터넷)에 요청을 보내게 된다.
특정 주소에 위치하는 서버(컴퓨터)에 요청을 보내고 해당 컴퓨터가 처리하고 돌려주는 응답을 돌려받는다.

 - 내부 네트워크 어댑터의 역할
이 과정에서 주소표시줄에 입력한 주소는 컴퓨터의 네트워크 어댑터(랜카드)가 해석하여 외부 네트워크로 전달해준다.

 - 루프백 주소로의 요청 전달
주소표시줄에 localhost 또는 127.0.0.1을 입력하면, 해당 요청은 네트워크 어댑터에서 외부로 나가는 대신
마치 외부에서 이 컴퓨터로 전달한 것처럼 내부 시스템에 전달된다.

 - 루프백 주소 요청 과정
1. 브라우저에 127.0.0.1:8000 입력
2. 네트워크 어댑터는 127.0.0.1 이라는 주소를 해석.
 - 127.0.0.1인 루프백으로, 외부가 아닌 내부 네트워크를 가리킨다.
3. 8000번 포트 해석
 - 랜카드는 내부 네트워크의 8000번 포트에서 실행되는 프로그램에 이 요청을 전달한다.
4. 8000번 포트에 개발서버로 전달된다.
 - 개발서버는 브라우저에서 전달한 요청을 처리하고, 응답한다.
5. 랜카드는 받은 응답을 요청의 근원지로 다시 전달한다.
 - 요청은 내부 네트워크의 브라우저에서 시작했으므로, 응답은 해당 브라우저로 전달된다.
6. 브라우저는 응답받은 결과를 표시한다.
```

<br/>

## Django 기본 사용법

### View 등록

 - `View 사용하기(Controller)`
    - 요청을 처리할 코드를 작성한다.
```py
# config/views.py
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, World!")
```

 - `URLconf 구현`
    - 설정 파일에 엔드포인트를 정의하고, 코드와 매칭시킨다.
```py
# config/urls.py
from django.contrib import admin
from django.urls import path
from config.views import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello", hello) # "hello" 엔드포인트에 hello 메서드 매칭
]
```

<br/>

### 템플릿 등록

 - `Template 사용하기`
    - 설정 파일에 템플릿 경로를 추가한다.
```py
# config/settings.py
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates" # 루트 폴더에서 템플릿 폴더 경로 설정

..

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR], # Template을 찾을 경로 추가
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

 - `Template 화면 작성`
    - '/templates/hello.html' 파일을 만든다.
```HTML
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Hello</title>
</head>
<body>
    <h2>Hello World!</h2>
</body>
</html>
```

 - `View 수정`
    - View(Controller)에서 템플릿 화면을 반환하도록 수정한다.
    - 템플릿 화면을 반환하기 위해서는 django.shortcuts.render 함수를 사용한다.
```py
from django.shortcuts import render

def hello(request):
    return render(request, "hello.html")
```

<br/>

## Model 구성하기

 - `새 Application 생성`
    - burgers 애플리케이션을 만들고, models.py에 Model 클래스를 작성한다.
```Bash
(venv) python manage.py startapp burgers
```

 - `새 Application을 Django에 등록`
    - 생성한 애플리케이션 정보를 Django 프로젝트에 알려주어야 한다.
    - config/settings.py에 INSTALLED_APPS 항목을 수정한다.
```py
# config/settings.py

INSTALLED_APPS = [
    "burgers",
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

 - `Model 클래스 구현`
    - Model 역할을 하는 클래스를 만들기 위해서는 Django에 내장된 models.Model 클래스를 상속받아야 한다.
    - Django 모델 데이터 유형: https://docs.django.ac/models/field-types
```py
from django.db import models

class Burger(models.Model):
    name = models.CharField(max_length = 20)
    price = models.IntegerField(default = 0)
    calories = models.IntegerField(default = 0)
```

 - `마이그레이션 생성과 적용`
    - Django는 기본적으로 회원가입과 로그인 기능을 제공한다. 해당 기능을 사용하기 위해서는 데이터베이스를 만들어주어야 한다.
    - Django는 기본적으로 특별 설정 없이 SQLite를 사용할 수 있다. migrate 명령어를 입력하면 기본 테이블 데이터를 생성해준다.
    - 그 외 Model에 정의한 클래스 정보를 테이블에 마이그레이션을 하기 위해서는 마이그레이션 파일을 만들고, 데이터베이스에 적용하는 과정을 거쳐야 한다.
        - 마이그레이션 파일을 생성하는 manage.py의 명령어는 makemigrations 이다.
        - 하나의 Model 클래스가 아닌, app 단위로 생성된다.
```Bash
# Django 기본 테이블 마이그레이션
(venv) python manage.py migrate

# Burger 클래스 마이그레이션
# 명령어 입력시 0001_initial.py 마이그레이션이 생성된다.
(venv) python manage.py makemigrations burgers

# 생성된 마이그레이션 파일로 데이터베이스에 적용한다.
(venv) python manage.py migrate burgers
```

<br/>

## Django admin 사용하기

Django는 개발자나 사이트를 사용하는 사람들이 쉽게 데이터를 편집할 수 있는 관리자 페이지를 제공하며 이를 Django admin 이라 부른다.  
 - 공식 문서: https://docs.django.ac/admin

<br/>

 - `admin.py 구현`
    - Burger 클래스를 다룰 수 있는 관리자 페이지를 만든다.
    - 'burgers/admin.py' 파일을 수정한다.
```py
from django.contrib import admin
from burgers.models import Burger

@admin.register(Burger)
class BurgerAdmin(admin.ModelAdmin):
    pass

```

 - `Admin 계정 만들기`
```Bash
(venv) python manage.py createsuperuser
Username (leave blank to use 'pc'): django
Email address: django@django.ac
Password: 
Password (again):
```

<br/>

## 데이터베이스 다루기

 - `Django 코드를 포함한 파이썬 인터프리터 실행`
    - python 명령어로 실행한 인터프리터에는 Django 프로젝트의 내용이 포함되지 않는다.
    - Django 프로젝트의 코드를 포함하기 위해서는 manage.py를 사용한다.
```Bash
(venv) python manage.py shell
```

 - `Django ORM 실습`
    - objects.all(): 테이블의 전체 데이터 조회
    - objects.get(name="값"): name 컬럼이 값과 동일한 데이터 조회
    - objects.filter(name__endswith="값"): name 컬럼이 특정 값으로 끝나는 데이터 조회
```Bash
# Burger 클래스 import
>>> from burgers.models import Burger

# 테이블 전체 데이터 조회
>>> Burger.objects.all()
<QuerySet [<Burger: 더블와퍼>, <Burger: 트러플머쉬룸X>, <Burger: 통새우와퍼>]>

# 특정 조건을 만족하는 데이터 조회
>>> burger = Burger.objects.get(name="더블와퍼")
>>> burger.id
1
>>> burger.name
'더블와퍼'
>>>burger.calories
842

# 특정 조건을 만족하는 데이터들 조회
>>> burgers = Burger.objects.filter(name__endswith="와퍼")
>>> burgers
<QuerySet [<Burger: 더블와퍼>, <Burger: 통새우와퍼>]>
>>> type(burgers)
<class 'django.db.models.query.QuerySet'>

# QuerySet 객체는 리스트처럼 다룰 수 있다. (초과 인덱스를 접근하면 IndexError 발생)
>>> len(burgers)
2
>>> burgers[0]
<Burger: 더블와퍼>

# QuerySet 객체 for문 순회
>>> for burger in burgers:
        print(burger.id, burger.name, type(burger))
```

<br/>

## View에서 데이터 다루기

 - `데이터를 가져오는 과정`
    - 사용자 URL 요청
    - URLconf가 전달받은 URL을 해석하여 요청에 해당하는 View 함수를 호출
    - View 함수는 Model 클래스를 통해 데이터를 조회
    - View 함수는 가져온 데이터를 Template에 전달
    - Template는 View에서 전달된 데이터를 사용해 동적인 HTML 생성
    - 생성한 HTML을 View 함수의 return에 의해 브라우저로 반환

<br/>

 - `View 함수에서 데이터 가져오기`
```py
# config/urls.py
from django.contrib import admin
from django.urls import path
from config.views import hello
from config.views import burger_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", hello),
    path("burgers/", burger_list)
]

# view.py
from django.http import HttpResponse
from django.shortcuts import render
from burgers.models import Burger

def hello(request):
    return render(request, "hello.html")

def burger_list(request):
    burgers = Burger.objects.all()
    
    # Template로 전달해줄 dict 객체
    context = {
        "burgers": burgers
    }
    
    return render(request, "burger_list.html", context)
```

 - `Template에서 데이터 다루기`
    - 변수: {{변수명}}
    - 태그: {% %}
```HTML
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>burger_list</title>
</head>
<body>
    <h1>햄버거 목록</h1>
    {% for burger in burgers %}
        <div>{{ burger.name }}</div>
        (가격: {{ burger.price }}원, 칼로리: {{ burger.calories }}kcal)
    {% endfor %}
</body>
</html>
```

<br/>

## Django에 데이터 전송하기

 - views.py
    - GET 파라미터를 처리하는 함수
```py
def burger_search(request):
    # 쿼리스트링으로 전달된 매개변수를 request.GET으로 받는다.
    # QueryDict 객체가 반환된다
    print(request.GET)

    keyword = request.GET.get("keyword") # 값이 없으면 None 객체 할당
    if keyword is not None:
        # keyword 값으로 검색된 QuerySet 할당
        burgers = Burger.objects.filter(name__contains=keyword)

    else:
        # 검색 결과가 없으면 빈 QuerySet 할당
        burgers = Burger.objects.none()

    context = {
        "burgers": burgers
    }

    return render(request, "burger_search.html", context)
```

 - urls.py
    - 엔드포인트와 함수 매칭
```py
from django.contrib import admin
from django.urls import path
from config.views import hello, burger_list, burger_search

urlpatterns = [
    path('admin/', admin.site.urls),
    path("hello/", hello),
    path("burgers/", burger_list),
    path("search/", burger_search)
]
```

 - burger_search.html
```HTML
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>burger_search</title>
</head>
<body>
    <h1>햄버거 검색화면</h1>
    <div>
        <form method="GET">
            <input type="text">
            <button>검색</button>
        </form>
    </div>
    <h2>검색결과</h2>
    {% for burger in burgers %}
        <div>{{ burger.name }}</div>
        (가격: {{ burger.price }}원, 칼로리: {{ burger.calories }}kcal)
    {% endfor %}
</body>
</html>
```
