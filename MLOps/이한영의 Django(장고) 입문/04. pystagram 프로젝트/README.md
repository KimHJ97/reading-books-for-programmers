# 04장. pystagram 프로젝트

## 개발 환경 구성

 - `Django 설치 및 초기설정`
    - 가상 환경을 통해 Django를 설치해주고, 이미지를 다루기 위해 Pillow 이미지 처리 라이브러리도 설치해준다.
    - Django 4.x 버전과 호환되는 10 미만 버전으로 설치한다.
```Bash
$ python -m venv pystagram
$ .\pystagram\Scripts\activate
(venv) pwd
(venv) pip install 'django<5'
(venv) pip install 'Pillow<10'
(venv) django-admin startproject config .
```

<br/>

 - `config/settings.py`
    - 템플릿 경로, 정적 파일 경로, 업로드 정적 파일 경로를 지정해준다.
    - 업로드 정적 파일 경로 처리를 위해 추가적으로 config/urls.py 파일도 변경해준다.
```py
# config/settings.py
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",        "DIRS": [TEMPLATES_DIR], # 템플릿 경로 설정
        ..
    }
]

..

STATIC_URL = "static/" # config/settings.py 하단에 기본적으로 정의되어 있음
STATICFILES_DIRS = [BASE_DIR / "static"] # 정적 파일 경로 설정

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.parent / "pylog_media" # 업로드 정적 파일 경로 설정
```
```py
# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
]
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
```

<br/>

 - `인덱스 페이지 구성`
```py
# config/views.py
from django.shortcuts import render

def index(request):
    return render(request, "index.html")
```
```HTML
<!-- templates/index.html -->
{% load static %}
<!doctype html>
<html lang="ko">
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <div id="index">
        <h1><a href="/posts/">pystagram</a></h1>
    </div>
</body>
</html>
```

<br/>

## 인증 시스템

Django는 기본적으로 로그인을 처리할 수 있는 기본 User 모델을 지원한다.  
기본 User 모델은 ID와 비밀번호, 이름 같은 최소한의 정보만을 지원한다. 사용자 모델에 추가 정보를 저장하고 싶다면 별도의 User 모델을 구성해야 한다.  

Django는 AbstractUser를 제공하며, 기본적으로 username, password, first_name, last_name, email, is_staff, is_active, date_joined, last_login 필드를 가진다.  
AbstractUser를 삭송받으면 자동적으로 해당 필드들을 가지고, 

 - CustomUser 모델 설정
    - __users 앱 생성 및 등록__
        - CustomeUser를 정의할 app을 만들고, settings.py에 등록한다. 어떤 User 모델을 사용하는 지도 정의한다. 언어와 시간대도 한국으로 설정해준다.
        - python manage.py startapp users
        - python manage.py makemigrations
        - python manage.py migrate
```py
# config/settings.py
from pathlib import Path

AUTH_USER_MODEL = "users.User"

.. 

INSTALLED_APPS = [
    "users",
    ..
]

# Internationalization
LANGUAGE_CODE = "ko-kr" # 기본값: en-us
TIME_ZONE = "Asia/Seoul" # 기본값: UTF

# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    profile_image = models.ImageField("프로필 이미지", upload_to="users/profile", blank=True)
    short_description = models.TextField("소개글", blank=True)


# users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = [
        (
            None,
            {
                "fields": ("username", "password"),
            },
        ),
        ("개인정보", {"fields": ("first_name", "last_name", "email")}),
        (
            "추가필드",
            {
                "fields": ("profile_image", "short_description"),
            },
        ),
        (
            "권한",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        (
            "중요한 일정",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    ]
```

<br/>

## 로그인/피드 페이지 기본 구조

 - `URLconf`
    - 기본적으로 'config/urls.py'에 URLconf 정보를 등록한다.
    - 하지만, 모든 경로를 해당 파일에서 관리하는 것은 비효율적이다. 때문에, app 별로 urls.py 파일을 만들어 내용을 분리해준다.
    - 'users/**'로 들어오는 요청은 users 앱의 urls.py 에서 분기한다.
    - __추가 작업__
        - 글 목록을 보여줄 posts 앱도 생성하여 등록해준다.
        - python manage.py startapp posts
```py
# users/urls.py: users 앱의 엔드포인트 정의
from django.urls import path
from users.views import login_view

urlpatterns = [
    path("login/", login_view)
]


# config/urls.py: Django의 URLconf 설정에 등록해준다.
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from config.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("posts/", include("posts.urls")), # posts 앱 URLconf 등록
    path("users/", include("users.urls")), # users 앱 URLconf 등록
    path("", index),
]
# ..

```

<br/>

## 로그인 여부에 따른 접속 제한

 - `피드 페이지`
    - 파라미터로 전달받은 request에서 요청된 사용자 정보를 가져올 수 있고, 로그인된 사용자인지 여부를 확인할 수 있다.
    - request.user.is_authenticated를 통해 로그인 여부를 가져올 수 있으며, 로그인되면 True, 로그인이 안되어있으면 False를 반환한다.
```py
from django.shortcuts import render, redirect

def feeds(request):
    # 요청(request)으로부터 사용자 정보 가져오기
    user = request.user
    if not user.is_authenticated:
        return redirect("users:login")

     return render(request, "posts/feeds.html")
```
