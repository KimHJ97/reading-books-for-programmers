# Hello API 만들기

가상 환경을 만들고, fastapi 라이브러리를 설치한 이후에 해당 작업을 진행한다.  

<br/>

## uvicorn 설치

FastAPI로 작성한 프로그램을 실행하기 위해서는 FastAPI 프로그램을 구동할 서버가 필요하다.  
가상 환경에 접속한 후 비동기 호출을 지원하는 파이썬용 웹 서버인 유비콘(uvicorn)을 설치한다.

```bash
(venv) pip install "uvicorn[standard]"
```

<br/>

## Hello API 코드 작성

myapi 폴더 내부에 backend 라는 적절한 폴더를 만들고, 소스 코드를 작업한다.  

 - `main.py`
    - CORSMiddleware를 통해 CORS 정책을 설정할 수 있다.
    - @app.get() 으로 엔드포인트를 지정할 수 있다.
```python
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://127.0.0.1:5173",    # 또는 "http://localhost:5173"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/hello")
def hello():
    return {"message": "안녕하세요 파이보"}

```

 - `프로젝트 실행`
    - main:app에서 main은 main.py 파일을 의미하고 app은 main.py의 app 객체를 의미한다.
    - --reload 옵션은 프로그램이 변경되면 서버 재시작 없이 그 내용을 반영하라는 의미이다.
```bash
(venv) uvicorn main:app --reload
```

<br/>

## Svelte 웹 페이지 만들기

Svelte 프로젝트에서 App.svelte와 app.css 파일을 변경한다.  
App.svelte 내용은 아래와 같이 변경하고 app.css는 모두 지워준다.  

 - `App.svelte`
    - FastAPI의 hello API를 호출하여 돌려받은 값을 message 변수에 담고, 화면에 출력한다.
```html
<script>
  let message;

  fetch("http://127.0.0.1:8000/hello").then((response) => {
    response.json().then((json) => {
      message = json.message;
    });
  });
</script>

<h1>{message}</h1>
```

<br/>

 - `fetch 함수 다른 사용법`
```html
<script>
  async function hello() {
    const res = await fetch("http://127.0.0.1:8000/hello");
    const json = await res.json();

    if (res.ok) {
      return json.message;
    } else {
      alert("error");
    }
  }

  let promise = hello();
</script>

{#await promise}
  <p>...waiting</p>
{:then message}
  <h1>{message}</h1>
{/await}
```
