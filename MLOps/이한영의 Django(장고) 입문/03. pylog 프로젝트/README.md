# pylog 프로젝트

## 개발 환경 구성

 - `Django 설치 및 초기설정`
    - 가상 환경을 통해 Django를 설치해주고, 이미지를 다루기 위해 Pillow 이미지 처리 라이브러리도 설치해준다.
    - Django 4.x 버전과 호환되는 10 미만 버전으로 설치한다.
```Bash
$ python -m venv pylog
$ .\pylog\Scripts\activate
(venv) pwd
(venv) pip install 'django<5'
(venv) pip install 'Pillow<10'
(venv) django-admin startproject config .
```

<br/>

 - `config/settings.py`
    - 템플릿 경로, 정적 파일 경로, 업로드 정적 파일 경로를 지정해준다.
        - 정적파일이란 이미지/동영상/CSS 파일과 같은 변하지 않는 데이터를 뜻한다.
        - 그 외에 유저가 업로드하는 정적 파일은 User-Uploaded static file 이라고 부르는데, "/media/" 보통 접두어를 사용한다.
```py
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

<br/>

 - `config/urls.py`
    - 인덱스 페이지 구성과 MEDIA_URL 업로드 파일을 연결해준다.
    - 템플릿에서 정적 파일을 불러올 떄 {% static '정적파일경로' %} 태그를 사용한다.
    - __MEDIA_URL 업로드 파일 연결__
        - MEDIA_URL로 시작하는 URL 요청이 오면, MEDIA_ROOT에서 파일을 찾아 돌려준다.
        - prefix: 어떤 URL 접두어가 올 경우
        - document_root: 어디에서 파일을 찾아 돌려줄 것인가
```py
# config/views.py
from django.shortcuts import render

def index(request):
    return render(request, "index.html")

# config/urls.py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from config.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
]
urlpatterns += static(
    # URL의 접두어가 MEDIA_URL일 때는 정적 파일을 돌려준다.
    prefix=settings.MEDIA_URL,
    # 돌려줄 디렉토리는 MEDIA_ROOT를 기준으로 한다.
    document_root=settings.MEDIA_ROOT,
)
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
        <h1><a href="/posts/">pylog</a></h1>
    </div>
</body>
</html>
```

<br/>

## 게시글 및 댓글 모델 구현

 - `모델 클래스 정의하기`
    - python manage.py startapp blog 명령어를 수행하고, config/settings.py에 등록한다. (INSTALLED_APPS 항목)
    - __테이블 설계__
        - 게시글(Post): id, title, content, thumbnail
        - 댓글(Comment): id, post_id, content
    - __코드 설명__
        - Comment 모델의 post 필드는 다른 모델(테이블)과의 1:N 연결을 구성해주는 ForeignKey 필드를 사용한다. 해당 필드는 연결된 Post 테이블 Row의 ID 값을 갖는다.
    - __테이블 생성__
        - Model 클래스를 작성하고, manage.py 명령어를 통해 테이블을 생성한다.
        - python manage.py makemigrations
        - python manage.py migrate
    - __Django ORM 설명__
        - Comment는 자신의 post 속성으로 연결된 Post 객체에 접근할 수 있다. 이를 정방향 관계라고 하며, 반대로 1:N 관계에서 Post가 Comment에 접근하는 것을 역방향 관계라 한다.
        - 역방향 접근을 위한 속성은 {N방향 모델명의 소문자}_set 이라는 이름으로 Django ORM이 자동으로 생성해준다.
        - 정방향 접근: Comment.objects.first().post
        - 역방향 접근: Post.objects.first().comment_set
            - 역방향 접근은 RelatedManager 객체를 이용한다. 1:N 관계에서 N개가 반환될 수 있기 때문에 Manager 객체를 통해서 접근한다.
            - post = Post.objects.first()
            - for comment in post.comment_set.all()
        - ImageFiled 속성들
            - post.thumbnail
            - post.thumbnail.name: MEDIA_ROOT 디렉토리 기준으로 이미지의 전체 경로
            - post.thumbnail.path: 시스템 전체를 기준으로 이미지 전체 경로
            - post.thumbnail.size: Bytes 사이즈
            - post.thumbnail.url: MEDIA_URL을 기준으로 이미지의 접근 URL
```py
from django.db import models

class Post(models.Model):
    title = models.CharField("포스트 제목", max_length=100)
    content = models.TextField("포스트 내용")
    thumbnail = models.ImageField("썸네일이미지", upload_to="post", blank=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField("댓글 내용")

    def __str__(self):
        return f"{self.post.title}의 댓글 ID: {self.id})"

```

<br/>

 - `Django Admin 등록`
    - Post(글)과 Comment(댓글)을 장고 어드민으로 쉽게 조작할 수 있도록 "blog/admin.py"에 등록해준다.
    - __어드민 계정 만들기__
        - manage.py 명령어로 어드민 계정을 만들어준다.
        - python manage.py createsuperuser
```py
from django.contrib import admin
from blog.models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "thumbnail"]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

```

<br/>

## 글과 댓글 기능 구현

 - `config/urls.py`
    - posts: 게시글 목록 페이지
    - posts/${post_id}: 게시글 상세 페이지 (동적 경로 값을 받는다.)
    - posts/add: 게시글 추가 페이지
```py
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from blog.views import post_list, post_detail, post_add
from config.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index),
    path("posts/", post_list),
    path("posts/<int:post_id>/", post_detail),
    path("posts/add/", post_add),
]
urlpatterns += static(
    prefix=settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)
```

 - `게시글 목록 페이지 구현`
```py
# blog/views.py
from blog.models import Post, Comment

def post_list(request):
    posts = Post.objects.all() # 모든 게시글 조회
    context = {
        "posts": posts,
    }
    return render(request, "post_list.html", context)
```
```HTML
<!-- templates/post_list.html -->
{% load static %}
<!doctype html>
<html lang="ko">
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <div id="navbar">
        <span>pylog</span>
        <a href="/posts/add/" class="btn btn-primary">글 작성</a>
    </div>
    <div id="post-list">
        <ul class="posts">
            {% for post in posts %}
                <li class="post">
                    <div><a href="/posts/{{ post.id }}/">{{ post.title }}</a></div>
                    <p>{{ post.content }}</p>
                    <ul class="comments">
                        {% for comment in post.comment_set.all %}
                            <li class="comment">{{ comment.content }}</li>
                        {% empty %}
                            <li class="comment-empty">아직 댓글이 없습니다</li>
                        {% endfor %}
                    </ul>
                    {% if post.thumbnail %}
                        <img src="{{ post.thumbnail.url }}" alt="">
                    {% else %}
                        <img src="" alt="">
                    {% endif %}
                </li>
            {% endfor %}
        </ul>
    </div>
</body>
</html>

```

<br/>

 - `글 상세 페이지 구현`
    - 경로 변수로 post_id를 받고, 해당 id에 해당하는 게시글을 조회한다.
    - 요청 Method가 POST인 경우 댓글 작성 로직을 처리한다.
```py
# blog/views.py
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        comment_content = request.POST["comment"]
        Comment.objects.create(
            post=post,
            content=comment_content,
        )

    context = {
        "post": post,
    }
    return render(request, "post_detail.html", context)
```
```HTML
<!-- templates/post_detail.html -->
{% load static %}
<!doctype html>
<html lang="ko">
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <div id="navbar">
        {% if post.thumbnail %}
            <img src="{{ post.thumbnail.url }}">
        {% endif %}
        <span>{{ post.title }}</span>
    </div>
    <div id="post-detail">
        <p>{{ post.content|linebreaksbr }}</p>
        <ul class="comments">
            {% for comment in post.comment_set.all %}
                <li class="comment">{{ comment.content }}</li>
            {% empty %}
                <li class="comment-empty">아직 댓글이 없습니다</li>
            {% endfor %}
        </ul>
        <form method="POST">
            {% csrf_token %}
            <textarea name="comment"></textarea>
            <button type="submit" class="btn btn-primary">댓글 작성</button>
        </form>
    </div>
</body>
</html>

```

<br/>

 - `글 작성 페이지 구현`
    - GET 방식인 경우 게시글 작성 페이지에 진입한 것이고, POST 방식인 경우 게시글 등록 로직을 수행한다.
    - __Django CSRF__
        - GET 방식의 요청은 사이트의 특정 페이지에 접속하거나, 검색을 하는 등의 읽기/조회 행동을 수행하는 데 쓰인다. 반면에 POST 방식의 요청은 사이트의 특정 데이터를 작성/변경하는데 쓰인다.
        - 기본적으로 Django는 POST 요청에 대해 CSRF 보안을 적용한다. CSRF 공격 방어의 핵심은 록읜한 사용자가 의도하지 않은 POST 요청을 거부하는 것이다. 이를 위해서 해커가 임의의 POST 요청을 할 수 없도록 Django는 새로운 요청을 하는 브라우저마다 구분되는 값을 서버에 저장하고, POST 요청을 하는 form이 브라우저별로 구분되는 값을 가지지 않는다면, 요청을 거부한다.
        - Template 영역에 {% csrf_token %} 태그를 사용하여, 브라우저별로 구분되는 값을 보내도록 할 수 있다. (CSRF Token) 해당 태그는 사용자에게 실제로 화면이 그려질 때 input hidden 태그로 토큰 값을 만들어준다.
    - __Django 파일 처리__
        - "multipart/form-data"로 파일을 전달받은 경우 request.FILES를 이용한다. 이때, 전달된 InMemoryUploadedFile은 Django에 내장된 File을 다루기 위한 클래스이다.
```py
from django.shortcuts import render, redirect
from blog.models import Post, Comment

# ..

def post_add(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        thumbnail = request.FILES["thumbnail"]
        post = Post.objects.create(
            title=title,
            content=content,
            thumbnail=thumbnail,
        )
        return redirect(f"/posts/{post.id}/")

    return render(request, "post_add.html")

```
```HTML
{% load static %}
<!doctype html>
<html lang="ko">
<head>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
</head>
<body>
    <div id="navbar">
        <span>글 작성</span>
    </div>
    <div id="post-add">
        <form method="POST" enctype="multipart/form-data">
            {% csrf_token %}
            <div>
                <label>제목</label>
                <input name="title" type="text">
            </div>
            <div>
                <label>내용</label>
                <textarea name="content"></textarea>
            </div>
            <div>
                <label>썸네일</label>
                <input name="thumbnail" type="file">
            </div>
            <button type="submit" class="btn btn-primary">작성</button>
        </form>
    </div>
</body>
</html>

```
