# 01장. FastAPI 개발 준비

## FastAPI

FastAPI는 Python 웹 프레임워크로, 특히 API 서버를 빠르고 쉽게 작성할 수 있도록 설계된 프레임워크입니다. FastAPI는 현대적이며 성능이 우수하며 자동 문서화 기능이 내장되어 있어 개발자가 API를 사용하고 이해하기 쉽습니다.  

FastAPI는 주로 API 서버를 개발할 때 사용되며, 데이터베이스와의 통합, 비동기 작업, 웹 소켓 지원 등 다양한 기능을 제공합니다. FastAPI는 Flask 및 Django와 같은 다른 Python 웹 프레임워크와 비교하여 성능 면에서 우수하며, 현대적이고 Pythonic한 문법을 통해 개발자 경험을 향상시킵니다.  

 - Fast: 비동기 처리(AsyncIO)를 활용하여 높은 성능을 제공합니다.
 - Type Hinting: Python 3.7 이상에서 지원되는 타입 힌팅을 사용하여 타입에 대한 명시성을 높입니다. 이는 코드의 가독성을 높이고 디버깅을 용이하게 합니다.
 - Automatic Documentation: FastAPI는 자동으로 OpenAPI 및 JSON 스키마 문서를 생성합니다. Swagger UI 및 ReDoc과 같은 도구를 사용하여 시각적으로 API를 탐색할 수 있습니다.
 - Dependency Injection: 의존성 주입을 지원하여 코드의 모듈화 및 유지보수를 용이하게 합니다.
 - Security: 보안 기능을 내장하고 있어, 입력 유효성 검사, OAuth 및 JWT 인증 등의 보안 기능을 손쉽게 적용할 수 있습니다.

<br/>

### 개발 환경 준비

 - `파이썬 설치`

FastAPI는 파이썬으로 만든 웹 프레임워크로 FastAPI를 구동하려면 반드시 파이썬을 먼저 설치해야 한다.  

```
1. 파이썬 공식 홈페이지 접속
 - https://www.python.org

2. 파이썬 설치 파일 다운로드
 - www.python.org/downloads

3. 파이썬 설치
 - Install Now(Add Python 3.x to PATH)
 - 전역으로 python 명령을 수행하기 위해 경로 등록 옵션에 체크해준다.

4. 파이썬 설치 확인
$ python -v
```

<br/>

 - `가상환경 만들기`

가상 환경은 파이썬 프로젝트를 진행할 때 독립된 환경을 만들어주는 도구이다.  
만약, 하나의 PC에 여러 버전이 다른 라이브러리를 사용하는 파이썬 프로젝트를 구축할 때 버전 문제가 발생할 수 있다.  
파이썬 가상 환경을 이용하면 하나의 PC 안에 독립된 가상 환경을 여러 개 만들 수 있다.  

예제로는 venvs 디렉토리를 만들어 가상 환경의 루트 디렉토리로 사용한다. 만약, 또 다른 가상 환경을 추가하고 싶다면 해당 디렉토리 아래에 설치한다.  

```bash
# 적당한 폴더 생성
$ mkdir venvs
$ cd venvs
$ python -m venv myapi

# 가상 환경 진입하기
$ cd C:\venvs\myapi\Scripts
$ activate

# 가상 환경에 FastAPI 설치
(myapi) pip install fastapi
(myapi) python -m pip install --upgrade pip

# 가상 환경 벗어나기
(myapi) C:\venvs\myapi\Scripts> deactivate

```

 - `배치 파일 만들고, 환경 변수에 추가하기`

가상 환경에 진입하기 위해서는 매번 명령 프롬프트를 실행하고 'C:\venvs\myapi\Scripts' 디렉토리에 있는 activate 명령을 수행해야 한다.  
이런 일련의 과정을 수행할 수 있는 배치 파일을 만들어 편리하게 이용할 수 있다.  

```bash
# myapi.cmd 파일 만들기
@echo off
cd c:/projects/myapi
c:/venvs/myapi/scripts/activate

# 배치 파일(*.cmd)을 환경 변수에 추가하기
# 시스템 환경 변수 > 고급 > 환경 변수(N) > Path > 새로 만들기 > C:\venvs

# 배치로 가상 환경 접속하기
$ myapi
```

<br/>

## Svelte


Svelte는 JavaScript 프레임워크로, 사용자 인터페이스를 빌드하기 위한 프론트엔드 프레임워크입니다. Svelte는 다른 프론트엔드 프레임워크와 다르게 빌드 시점에 컴파일되어 최적화된 네이티브 JavaScript 코드로 변환되며, 런타임에 별도의 프레임워크 코드가 필요하지 않습니다.  

Svelte는 Vue.js, React, Angular와 같은 다른 프론트엔드 프레임워크와 경쟁하고 있으며, 특히 빌드된 결과물이 경량이고 빠르다는 점에서 주목을 받고 있습니다.  

 - Write less code - 다른 프론트엔드 프레임워크에 비하여 작성해야 할 코드들이 적다. 어떤 기능을 구현하기 위해 가독성은 떨어지지만 어쩔 수 없이 작성해야 하는 틀에 짜인 코드를 boilerplate 코드라고 하는데 Svelte는 이러한 부분들이 거의 없다. 단순하고 이해하기 쉬운 코드만이 존재한다.
 - No virtual Dom - React나 Vue.js와 같은 프레임워크는 가상돔을 사용하지만 Svelte는 가상돔을 사용하지 않는다. Svelte는 가상돔을 사용하지 않는 대신 실제 Dom을 반영한다. Svelte는 앱을 실행 시점(Run time)에서 해석하지 않고 빌드 시점(Build time)에서 Vanilla JavaScript Bundle로 컴파일하여 속도가 빠르고 따로 라이브러리를 배포할 필요가 없어 간편하다.
 - Truly reactive - 복잡한 상태 관리를 위한 지식 및 라이브러리들이 필요없다. Svelte는 순수 자바스크립트만으로 그 기능을 이해하기 쉽게 구현했다.

```bash
# Svelte 애플리케이션 템플릿 만들기
$ npm create vite@latest frontend -- --template svelte

# Svelte 애플리케이션 설치
$ cd frontend
$ npm install

# Svelte 서버 실행
$ npm run dev
```

Svelte 프로젝트 안에 jsconfig.json 파일에 checkJs 옵션을 false로 해준다.  
스벨트는 기본적으로 자바스크립트 타입을 체크하도록 되어있다. Typescript를 사용하지 않을 경우 해당 옵션을 false로 해준다.  

```json
{
  "compilerOptions": {
    (... 생략 ...)
    /**
     * Typecheck JS in `.svelte` and `.js` files by default.
     * Disable this if you'd like to use dynamic types.
     */
    "checkJs": false
  },
  (... 생략 ...)
}
```

