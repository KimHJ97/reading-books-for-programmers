# 19. 실전 프로젝트 환경 구성

타입스크립트 프로젝트를 구성하기 위해서는 타입스크립트 설정 파일과 선언 파일, 빌드 도구를 타입스크립트와 함께 사용하는 방법을 알아야 한다.  

<br/>

---
## 19.1 타입스크립트 설정 파일

타입스크립트 설정 파일은 해당 타입스크립트 프로젝트가 어떻게 컴파일될지 세부적인 옵션을 정의하는 파일이다.  
예를 들어 컴파일할 대상 파일이나 폴더, any 타입의 사용 여부, 모듈 형태, 컴파일 결과물의 위치 등 다양한 옵션을 정의할 수 있다.  
타입스크립트 설정 파일은 타입스크립트 프로젝트의 루트 레벨에 위치해야 하며 JSON 파일 형식으로 작성한다.  

<br/>

---
## 19.2 타입스크립트 설정 파일 생성

타입스크립트 설정 파일을 만들 때 tsc 명령어를 이용하면 쉽게 만들 수 있다.  
tsc 명령어를 사용하기 위해서는 타입스크립트 라이브러리를 시스템 전역 레벨에 설치하거나 npx 명령어를 사용해야 한다.  
 - npx는 Node Package eXecute의 약어로 NPM 패키지를 설치하지 않고도 실행할 수 있게 하는 도구이다.
```bash
# 타입스크립트 라이브러리를 전역 레벨에 설치
$ npm install typescript --global
$ tsc --init

# npx로 타입스크립트 명령어 실행
$ npx typescript tsc --init
```

<br/>

---
## 19.3 타입스크립트 설정 파일의 루트 옵션

루트 옵션은 컴파일할 대상 파일이나 폴더를 지정하는 등 프로젝트 전반적인 환경 구성과 관련된 옵션이다.  

<br/>

### 19.3.1 files

files 옵션은 타입스크립트 컴파일 대상 파일의 목록을 의미한다.  
tsc 명령어를 입력했을 때 대상이 되는 파일 목록을 지정할 수 있다.

 - 해당 옵션 속성은 실무에서 자주 사용되지 않는다.
 - 실무 프로젝트에서는 파일의 개수가 많기 떄문에 일일이 목록을 지정하기 보다 include 속성을 이용하여 특정 위치나 파일 패턴으로 컴파일 대상을 지정한다.
```JSON
// tsconfig.json
{
    "files": ["index.ts", "main.ts", "utils.ts"]
}
```

<br/>

### 19.3.2 include

include 옵션은 타입스크립트 컴파일 대상 파일의 패턴을 지정하는 속성이다.  
files 옵션 속성과는 다르게 특정 폴더 위치나 파일 확장자를 기준으로 정할 수 있다.
 - *: 디렉토리 구분자를 제외한 모든 파일
 - **/: 해당 폴더의 모든 하위 폴더
```JSON
// src 폴더 아래 모든 파일과 tests 폴더 아래 spec.ts 확장자를 가진 모든 파일을 컴파일 대상으로 지정
{
    "include": ["src/*", "tests/*.spec.ts"]
}

// src 폴더 아래에 있는 모든 파일(하위 폴더의 파일까지 모두 포함)과 utils 폴더 바로 아래에 있는 모든 파일을 컴파일 대상으로 지정
{
    "include": ["src/**/*", "utils/*"]
}
```

<br/>

### 19.3.3 exclude

exclude 옵션은 include 속성에 정의된 파일들을 검색할 때 컴파일에서 제외할 파일 목록을 정의할 수 있다.  
include 대상에서 특정 파일을 제외할 때 사용한다.
 - include 속성을 별도로 정의하지 않으면 '**/*' 로 설정되어 프로젝트 내 전체 파일을 모두 컴파일 대상으로 한다.
```JSON
{
    "include": ["**/*"],
    "exclude": ["node_modules", "test/**/*"]
}
```

<br/>

### 19.3.4 extends

extends 옵션은 여러 타입스크립트 프로젝트에서 설정 파일을 공통으로 사용하거나 빌드용 타입스크립트 설정을 분리하고 싶을 때 사용한다.  
 - 타입스크립트 설정 내용을 분리할 수 있다.
    - 테스트용 설정 옵션과 운영용 설정 옵션을 분리할 수 있다.
```JSON
// base.json
{
    "compilerOptions": {
        "target": "es5",
        "lib": ["dom", "esnext"]
    }
}

// tsconfig.json
{
    "extends": "./base",
    "compilerOptions": {
        "strict": true
    }
}

// 실제 적용된 내용: tsconfig.json 파일에서 base.json 파일의 내용을 상속받는다.
{
    "compilerOptions": {
        "target": "es5",
        "lib": ["dom", "esnext"],
        "strict": true
    }
}
```

<br/>

---
## 19.4 타입스크립트 설정 파일의 컴파일러 옵션

컴파일러 옵션은 타입스크립트 컴파일 작업을 진행할 때 타입 검사 레벨, 타입 라이브러리, 모듈 등 세부적인 내용을 정의할 수 있다.  
 - [타입스크립트 공식 문서](https://www.typescriptlang.org/tsconfig)

<br/>

### 19.4.1 target

target 속성은 타입스크립트 컴파일 겨과물이 어떤 자바스크립트 문법으로 변환될지 정의하는 옵션이다.  
1999년 자바스크립트 스팩인 ES3부터 최신 자바스크립트 문법 ESNext까지 가능하다.  
 - 최신 브라우저(크롬, 파이어폭스, 웨일, 엣지 등)에서는 최신 문법을 지원하기 때문에 ESNext로 해도 문제는 없다.
 - 하지만, 인터넷 익스플로러와 같은 구 버전 브라우저에서 동작해야 한다면 ES5로 설정해야한다.
```JSON
{
    "compilerOptions": {
        "target": "es5",
        //..
    }
}
```

<br/>

### 19.4.2 lib

lib 속성은 브라우저 DOM API나 자바스크립트 내장 API를 위해 선언해 놓은 타입 선언 파일을 의미한다.  
 - 브라우저 DOM API는 화면을 조작하는 document.querySelect() API나 비동기 처리를 위한 setTimeout() API 등을 의미한다.
 - 자바스크립트 내장 API는 Math, Promise, Set 등 자바스크립트 문법으로 지원되는 API를 의미한다.
```JSON
{
    "compilerOptions": {
        "target": "es5",
        "lib": ["dom", "esnext"],
        // ..
    }
}
```

<br/>

### 19.4.3 strict

strict 속성은 타입스크립트의 타입 체크 수준을 정의하는 옵션이다.  
엄격하게 체크할 것이라면 true, 유연하게 체크할 것이라면 false를 준다.
 - strict를 true로 하면, 여러 개의 컴파일러 옵션 속성을 정의한 것과 같다.
    - noImplicitAny: 타입 정의가 안 된 코드에서 경고를 표시하는 옵션으로 타입을 모른다면 any 타입으로라도 명시해야 한다.
    - noImplicitThis: this 타입이 암묵적으로 any 타입을 가리키면 에러를 표시하는 옵션이다.
    - strictNullChecks: null과 undefined 값이 모두 타입으로 취급되도록 타입 검사 수준을 높이는 옵션이다.
    - strictBindCallApply: 자바스크립트의 call(), bind(), apply() API를 사용할 때 인자 타입이 적절한지 검사하는 옵션이다.
    - strictFunctionTypes: 함수의 파라미터 타입을 엄격하게 검사하는 옵션이다.
    - strictPropertyInitialization: 클래스 안에서 속성 타입이 정의되고 생성자에서 초기화까지 되어 잇는지 검사하는 옵션이다.
    - alwaysStrict: use strict 모드로 파일을 컴파일하고, 컴파일한 파일 위에 'use strict' 코드를 추가하는 옵션이다.
    - useUnknownInCatchVariables: try catch 구문에서 catch의 err 파라미터 타입을 unknown으로 변환해 주는 옵션이다.
```JSON
{
    "compilerOptions": {
        // 다음 속성 하나를 켜면
        "strict": true,
        // 다음 속성 목록 전부를 켠 것과 같음
        "noImplicitAny": true,
        "noImplicitThis": true,
        "strictNullChecks": true,
        "strictBindCallApply": true,
        "strictFunctionTypes": true,
        "strictPropertyInitialization": true,
        "alwaysStrict": true,
        "useUnknownInCatchVariables": true
    }
}
```

<br/>

### 19.4.4 allowJs

allowJs 속성은 타입스크립트 프로젝트에서 자바스크립트 파일도 함께 사용하고 싶을 때 추가하는 옵션이다.  
기본적으로 꺼져 있지만, true 값으로 변경하여 옵션을 켜면 타입스크립트 컴파일 대상에 자바스크립트 파일도 포함된다.  
쉽게, 타입스크립트 파일에서 자바스크립트 파일을 가져올(import) 수 있게 된다.  

```TS
// math.js
export function sum(a, b) {
    return a + b;
}

// index.ts
import { sum } from './math';
console.log(sum(10, 20));
```

<br/>

### 19.4.5 sourceMap

sourceMap 속성은 소스맵이라는 기능을 켜고 끄는 옵션이다.  
소스맵이란 타입스크립트뿐만 아니라 프론트엔드 빌드 도구에서 흔하게 사용되는 기능으로써 디버깅을 편하게 하는 역할을 한다.  

<br/>

타입스크립트로 빌드(컴파일)하면 자바스킄립트 파일이 생성된다.  
이때 자바스크립트 파일에서 실행 에러가 발생하면 자바스크립트 코드 위치를 가리키게 된다.  
컴파일된 자바스크립트 파일은 이미 원본 파일인 타입스크립트 파일과 다른 파일이다.  
때문에, 실제 타입스크립트 코드 중에 어느 부분에서 에러가 난지 찾기가 어렵다.  

<br/>

이러한 문제를 해결해 주는 기능이 바로 소스맵이다.  
소스맵은 컴파일 결과물인 자바스크립트 파일에서 에러가 발생했을 때 해당 에러가 원본 파일의 몇 번째 줄인지 가리켜 준다.  
 - sourceMap 옵션을 true로 하고 index.ts 파일을 컴파일하면 index.js 뿐만 아니라 index.js.map 파일도 생성된다.
```JSON
{
    "compilerOptions": {
        "sourceMap": true
    }
}
```

<br/>

### 19.4.6 jsx

jsx 속성은 리액트와 관련 있는 옵션으로 타입스크립트 파일에서 작성된 jsx 문법이 자바스크립트 파일에서 어떻게 변환될지 결정할 수 있다.  
 - jsx란 자바스크립트 확장 문법인 "Javascript Syntax eXtension"을 의미한다.
    - preserve: jsx 코드를 별도의 API로 변환하지 않고 최신 자바스크립트 문법과 라이브러리만 추가해준다.
    - react: jsx 코드를 React.createElement() 문법으로 변환해준다.
    - react-jsx
    - react-jsxdev
    - react-native
```JS
// index.ts
function App() {
    return <div>Hello React</div>
}

// preserve 옵션
import React from 'react';
export const App = () => <div>Hello React</div>;

// react 옵션
import React from 'react';
export const App = () => React.createElement("div", null, "Hello React");

// react-jsx 옵션
import { jsx as _jsx } from 'react/jsx-runtime';
import React from 'react';
export cont App = () => _jsx("div", { children: "Hello React"});

// react-jsxdev
import { jsxDEV as _jsxDEV } from "react/jsx-dev-runtime";
const _jsxFileName = "/home/runner/work/TypeScript-Website/TypescScript-Website/index.tsx";
import React from 'react';
export const App = () => _jsxDEV("div", { children: "Hello React"}, void 0, false, { fileName: _jsxFileName, lineNumber: 9, columnNumber: 32 }, this);

// react-native
import React from 'react';
export const App = () => <div>Hello React</div>;
```

<br/>

### 19.4.7 baseUrl

baseUrl 속성은 프로젝트의 모듈 해석 기준 경로를 정하는 옵션이다.  
VSCode나 Web Storm 등 개발 툴에서 파일 자동 완성을 올바르게 지원받는 것과도 연관이 있다.  
```JS
// tsconfig.json
{
    "compilerOptions": {
        "baseUrl": "./src"
    }
}

// index.js
import { formatDate } from 'utils/format'; // src/utils/format.js 파일
```

<br/>

### 19.4.8 paths

paths 속성은 특정 모듈을 임포트할 때 어디서 가져올지 경로를 지정할 수 있는 옵션이다.  
상대 경로가 길어질 때 이를 줄이는 데 사용하는 속성으로 baseUrl 속성 값에 영향을 받는다.  
```JS
// tsconfig.json
{
    "compilerOptions": {
        "baseUrl": ".",
        "paths": {
            "jquery": ["node_modules/jquery/dist/jquery"]
        }
    }
}

// index.js
import $ from 'jquery'; // "./node_modules/jquery/dist/jquery" 경로
```

<br/>

### 19.4.9 removeComments

removeComments 속성은 타입스크립트 컴파일을 할 때 주석을 제거해 주는 옵션이다.  
따로 설정하지 않으면 기본적으로 false 값을 갖는다.
```JSON
{
    "compilerOptions": {
        "removeComments": true
    }
}
```

<br/>

---
## 19.5 타입스크립트 설정 파일과 빌드 도구

타입스크립트를 사용하는 프로젝트는 대부분 리액트(React)나 뷰(Vue.js) 같은 프론트엔드 개발 프레임워크와 웹팩(webpack) 또는 롤업(rollup) 이라는 빌드 도구를 사용한다.  
실무 프로젝트에서는 단순히 타입스크립트만 빌드하지 않고 아래 과정을 모두 하나의 비륻 과정에 포함시키기도 한다.  
 - 파일 변환: ts 파일을 js 파일로 변환하거나, 최신 js 문법을 예전 js 문법으로 변환하거나, scss 파일을 css 파일로 변환하는 등 빌드 작업을 의미한다.
 - 파일 압축: 페이지 로딩 속도를 높이려고 파일을 압축하여 용량을 줄인다.
 - 파일 병합: 여러 개의 파일을 하나의 파일로 병합하여 네트워크 요청 시간을 줄인다.

<br/>

### 19.5.1 웹팩이란?

웹팩은 모듈 번들러이자 프론트엔드 개발 빌드 도구이다.  
파일 여러 개와 모듈을 다루는 실무 프로젝트에서 거의 필수로 사용하는 도구이다.  
모듈 번들러는 여러 개의 모듈을 하나의 모듈로 병합해준다는 의미이다.  
웹팩은 애플리케이션을 구성하는 리소스(js, css, jpg 파일 등)를 각각 하나의 모듈로 취급한다.  
 - [웹팩 핸드북 가이드](https://joshua1988.github.io/webpack-guide/)

<br/>

### 19.5.2 웹팩에 타입스크립트 설정하기

 - 해당 코드는 CRA(Create React App), CNA(Create Next App), Vue CLI 처럼 프로젝트 생성 도구로 프로젝트를 생성하면 기본적으로 작성되어진다.
 - [웹팩 주요 속성](https://joshua1988.github.io/webpack-guide/concepts/overview.html)
    - entry: 웹팩의 진입점으로 웹팩 빌드 명령어를 실행햇을 때 대상이 되는 파일 경로를 지정한다.
    - module: 웹팩의 로더를 의미한다. 자바스크립트 파일을 제외한 css, jpg, ttf 파일들을 모듈로 취급하려면 로더를 설정해주어야 한다. 타입스크립트 파일 역시 자바스크립트 파일이 아니기 때문에 ts-loader를 설정해주어야 한다.
    - resolve: 웹팩의 모듈 해석 방식을 정의해준다. extensions에 적힌 파일 확장자는 import 구문을 사용할 때 파일 확장자를 적지 않아도 인식하겠다는 의미이다.
    - output: 웹팩으로 빌드된 결과물에 대한 설정이다. 빌드한 파일ㅇ 이름은 bundle.js이고, 빌드된 파일 경로는 dist 폴더 아래이다.
```JS
// webpack.config.js
const path = require('path');

module.exports = {
    entry: './src/index.ts',
    module: {
        rules: [
            {
                test: /\.tsx?$/,
                use: 'ts-loader',
                exclude: /node_modules/,
            },
        ],
    },
    resolve: {
        extensions: ['.tsx', '.ts', '.js'],
    },
    output: {
        filename: 'bundle.js',
        path: path.resolve(__dirname, 'dist'),
    },
};
```

<br/>

---
## 19.6 타입 선언 파일

타입 선언 파일은 d.ts 확장자를 갖는 타입스크립트 파일을 의미한다.  
프로젝트에서 자주 사용되는 공통 타입이나 프로젝트 전반에 걸쳐 사용하는 라이브러리 타입을 정의하는 공간이다.  

<br/>

### 19.6.1 타입 선언 파일 사용 방법

프로젝트 루트 레벨에 정의해 놓으면 자동으로 프로젝트 내 타입스크립트 파일에서 해당 타입을 인식한다.

```TS
// project.d.ts
interface Product {
    name: string;
    id: string;
}

// index.ts
const shirts: Product = {
    name: '와이셔츠',
    id: '1'
};
```

<br/>

### 19.6.2 타입 선언 파일을 언제 사용해야 하는가?

타입 선언 파일을 사용하면 타입스크립트 파일에 타입 코드를 작성하지 않고 다른 파일에 분리해 놓을 수 있는 이점이 있다.  
많은 곳에서 사용되는 공통 타입이 있는 경우 별도로 익스포트하거나 임포트하지 않고 프로젝트 레벨에서 자동으로 인식하게 할 수 있다.

<br/>

---
## 19.7 외부 라이브러리의 타입 선언과 활용

타입스크립트 프로젝트에서 외부 라이브러리를 사용할 때 알고 있어야 할 점이 있다.  
외부 라이브러리는 보통 자바스크립트 코드로 작성되어 있다.  
때문에, 타입스크립트의 타입이 적용되어 있지 않다.  

<br/>

### 19.7.1 외부 라이브러리를 사용하는 방법

타입스크립트 프로젝트는 빌드 과정이 있어서 보통 NPM 기반으로 프로젝트를 구성하고 외부 라이브러리를 설치한다.  
타입스크립트에서 외부 라이브러리 사용자들이 특정 라이브러리에 대한 타입을 정의해서 Definitely Typed라는 깃헙 리포지토리에 공유해 두었다.  
 - 쉽게, 타입스크립트에서 외부 라이브러리를 사용하기 위해서는 해당 외부 라이브러리가 제공하는 API 들에 대한 타입이 필요하다.
 - 그래서, 사람들이 많이 사용하는 라이브러리 타입을 누군가가 미리 정의해서 레포지토리에 모아 공유가 되어있다.
 - 해당 라이브러리는 타입 선언 패키지로 외부 라이브러리 API의 타입 정의가 되어있다.
    - 즉, 외부 라이브러리와 타입 선언 패키지를 설치해야한다.
 - [깃헙 저장소](https://github.com/DefinitelyTyped/DefinitelyTyped)
 - NPM 공식 사이트에서 패키지를 검색하여 타입 선언 파일을 지원하는지 확인하고, '@types/라이브러리명'으로 패키지가 있는지 확인한 후 프로젝트에 설치해서 사용하면 된다.
```bash
# jquery를 사용하는 경우
$ npm install jquery
$ npm install @types/jquery
```