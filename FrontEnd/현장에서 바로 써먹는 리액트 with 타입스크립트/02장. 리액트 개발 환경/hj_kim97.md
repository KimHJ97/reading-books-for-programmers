# 02. 리액트 개발 환경

## 2.1 윈도우 개발 환경 설정

### 2.1.1 초콜리티 설치

초킬리티는 윈도우에서 패키지를 설치하고 관리할 수 있는 윈도우용 패키지 관리자이다.  
초콜리티를 통해 윈도우에 필요한 패키지를 간단하게 설치할 수 있다.  
 - [초콜리티 설치 페이지](https://chocolatey.org/install#individual)

```
1. 초콜리티 사이트 접속

2. Now run the following command 복사
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

3. 파워 쉘(Power Shell) 관리자 권한으로 실행 후 명령어 입력
$ Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

4. 초콜리티 설치 확인
$ choco -version
```

<br/>

### 2.1.2 노드 설치

리액트는 자바스크립트 라이브러리로, 프로젝트를 생성하고 개발에 필요한 외부 라이브러리를 사용할 때에 노드 패키지를 이용한다.  
따라서 리액트를 개발하기 위해서는 노드 설치가 필요하다.  
윈도우용 패키지 관리자인 초콜리티를 통해 노드를 설치할 수 있다.  

```
$ choco install -y nodejs. install
$ node --version
$ npm --version
```

<br/>

## 2.2 맥 개발 환경 설정

### 2.2.1 홈브루 설치

홈브루는 맥에서 패키지를 설치하고 관리할 수 있는 맥용 패키지 관리자이다.  
홈브루를 통해 맥에 필요한 패키지를 간단하게 설치할 수 있다.  
 - [홈브루 사이트](https://brew.sh/)
```
1. 홈브루 설치
$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

2. 홈브루 설치 확인
$ brew --version
```

<br/>

### 2.2.2 노드 설치

맥용 패키지 관리자인 홈브루를 통해 노드를 설치할 수 있다.

```
$ brew install node
$ node -v
$ npm -v
```

<br/>

## 2.3 리액트를 시작하는 방법

리액트를 사용하여 프로젝트를 시작하는 방법은 여러가지가 있다.  
 - 스크립트 태그 추가
 - Webpack이나 Babel을 설정하여 개발
 - create-react-app
 - Next.js 프레임워크

<br/>

### 2.3.1 스크립트 태그 추가

리액트는 자바스크립트 라이브러리로 jQuery와 같은 라이브러리처럼 스크립트 태그를 추가하여 사용할 수 있다.  
스크립트 추가 방식은 쉽고 빠르게 기존의 웹 서비스에 리액트를 시작할 수 있다.  
하지만, Webpack, Babel 등을 사용하지 않으므로 모든 브라우저에서 동작하는 순수 자바스크립트로 리액트 코드를 작성해야 한다.
```HTML
<body>
    <div id="app"></div>

    <script crossorigin src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
</body>
```

<br/>

### 2.3.2 Webpack이나 Babel을 설정하여 개발

크로스 브라우징 문제와 최신 ECMAScript, TypeScript 등을 사용하여 리액트 프로젝트를 진행하기 위해서는 Webpack, Babel을 설치하여 개발해야 한다.  
하지만, 이 방법은 Webpack이나 Babel을 잘 알아야 하고, 많은 설정이 필요하다.  
때문에, 리액트만을 집중하여 개발하기 어렵고 처음 접하는 입문자에게는 큰 어려움으로 다가올 수 있다.
 - Webpack으로 리액트 시작하기: https://dev-yakuza.posstree.com/ko/react/start/

<br/>

### 2.3.3 create-react-app

create-react-app은 복잡한 Webpack이나 Babel을 설정하지 않아도 간단하게 리액트 프로젝트를 생성하고 개발할 수 있는 CLI 툴이다.  
 - create-react-app: https://create-react-app.dev/

<br/>

### 2.3.4 Next.js 프레임워크

리액트는 단순히 웹 서비스의 UI를 담당하는 자바스크립트 라이브러리이다.  
즉, 프레임워크가 아닌 라이브러리로 웹 서비스에서 다른 기능이 필요한 경우 외부 라이브러리와 함께 사용해야 한다.  
Next.js는 리액트로 웹 서비스를 만들 때에 주로 사용되는 기능들을 함께 묶어 제공하는 리액트 프레임워크이다.  
Next.js를 사용하면, react-router와 같은 외부 라이브러리를 사용하지 않고도 페이지 전환 기능을 사용할 수 있고, 서버 사이드 렌더링(SSR)과 같은 리치 기능도 제공한다.  

<br/>

## 2.4 create-react-app

```Bash
# create-react-app으로 프로젝트 생성 및 실행
$ npx create-react-app my-app

$ cd my-app
$ npm start
```

- create-react-app 프로젝트 폴더 구조
- package.json: 리액트 애플리케이션 개발에 필요한 라이브러리나 프로젝트에서 사용하는 명령어 스크립트를 관리하는 파일
    - public 폴더
        - 리액트 프로젝트에 필요한 HTML 파일과 favicon 등 정적인 파일
        - index.html: 리액트도 웹 서비스로 기본적으로 HTML 파일이 필요한데, 기본이 되는 HTML 파일
    - src 폴더
        - 실제로 리액트를 가지고 프로그래밍할 자바스크립트 파일(소스 코드)
        - reportWebVials.js: 리액트의 선응을 측정하기 위해 제공되는 파일
        - setupTests.js: 리액트 프로젝트를 테스트하는 데 필요한 설정 파일
```
├─ README.md
├─ package-lock.json
├─ package.json
├─ public
├   ├─ facivon.ico
├   ├─ index.html
├   ├─ logo192.png
├   ├─ logo512.png
├   ├─ manifest.json
├   └─ robots.txt
└─ src
    ├─ App.css
    ├─ App.js
    ├─ App.test.js
    ├─ index.css
    ├─ index.js
    ├─ logo.svg
    ├─ reportWebVitals.js
    └─ setupTests.js
```