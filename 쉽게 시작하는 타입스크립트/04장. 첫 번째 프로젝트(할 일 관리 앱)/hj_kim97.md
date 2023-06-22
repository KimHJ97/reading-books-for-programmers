# 4. 첫 번째 프로젝트(할 일 관리 앱)

## 4.1 프로젝트 내려받기 및 라이브러리 설치

링크를 통해 프로젝트를 받는다.  
할 일 관리 앱은 '1_todo' 폴더의 프로젝트를 사용한다.  
해당 폴더에 접근 후 'npm i'로 package.json의 설정된 내용으로 의존성 모듈들을 설치한다.
 - [프로젝트 코드 링크](https://github.com/joshua1988/learn-typescript)
 - [프로젝트 코드 링크](https://github.com/gitbutITbook/080316)

---
## 4.2 프로젝트 폴더 구조

<center> 
  <img src="./images/%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EA%B5%AC%EC%A1%B0.PNG" alt="프로젝트 구조" />
</center>

### 4.2.1 node_modules 폴더

node_modules 폴더에는 실습에 필요한 라이브러리가 설치된다.  
npm i 명령어를 입력해서 필요한 라이브러리를 설치하는데, 정상적으로 설치가 종료되면 node_modules 폴더가 생성된다.

### 4.2.2 src 폴더

소스 폴더로 타입스크립트 파일을 작성한다.

### 4.2.3 .slintrc.js 파일

.eslintrc.js 파일은 ESLint 설정 파일이다.  
ESLint란 자바스크립트의 문법 검사 도구를 의미한다.  
자바스크립트 코드를 일관된 형식으로 작성할 수 있게 도와주고 잠재적인 에러가 발생할 수 있는 코드에 경고를 해준다.  
또한, ESLint는 자바스크립트뿐만 아니라 추가적인 구성으로 타입스크립트 코드까지 검사할 수 있다.

### 4.2.4 package.json

package.json 파일은 NPM 설정 파일이다.  
NPM 설정 파일은 프로젝트 이름, 버전, 라이선스 등 프로젝트와 관련된 기본 정보가 들어간다.  
또한, 프로젝트를 실행하거나 로컬에서 개발할 때 필요한 라이브러리 목록을 저장할 수 있다.  
 - name: 프로젝트 이름
 - version: 프로젝트 버전
 - description: 프로젝트 설명
 - main: 프로젝트 메인 파일
 - scripts: 프로젝트 명령어. 임의로 명령어를 생성해서 'npm run 명령어' 형태로 해당 명령어를 실행 가능
 - keywords: NPM 사이트에서 검색할 때 연관될 검색어
 - author: 프로젝트 작성자
 - license: 프로젝트 라이선스 종류 표기
 - devDependencies: 프로젝트를 로컬에서 개발할 때 도움을 주는 라이브러리 목록.
    - ex) 로컬에서 사용할 개발 서버나 코드 문법 검사 도구 등이 해당된다.
```JSON
{
  "name": "1_todo",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC",
  "devDependencies": {
    "@babel/core": "^7.9.0",
    "@babel/preset-env": "^7.9.5",
    "@babel/preset-typescript": "^7.9.0",
    "@typescript-eslint/eslint-plugin": "^2.27.0",
    "@typescript-eslint/parser": "^2.27.0",
    "eslint": "^6.8.0",
    "eslint-plugin-prettier": "^3.1.2",
    "prettier": "^2.0.4",
    "typescript": "^3.8.3"
  }
}
```

### 4.2.5 package-lock.json 파일

package-lock.json 파일은 dependencies나 devDependencies에 명시된 라이브러리를 설치할 때 필요한 부수 라이브러리의 버전을 관리한다.  
package.json 파일에 명시된 라이브러리를 설치하고 나면 자동으로 생성된다.
 - 개발자가 직접 package-lock.json 파일의 내용을 수정하지 않는다.

### 4.2.6 tsconfig.json 파일

tsconfig.json 파일은 타입스크립트 설정 파일이다.  
타입스크립트 프로젝트는 기본적으로 최상위 폴더 아래에 타입스크립트 설정 파일이 존재한다.  
이 설정 파일에는 타입스크립트 컴파일을 돌릴 파일 목록과 배제할 목록, 컴파일러를 구체적으로 어떻게 동작시킬지 등 다양한 옵션을 지정할 수 있다.
 - compilerOptions: 타입스크립트로 컴파일할 때 세부적인 동작을 지정할 수 있는 옵션
    - allowJs: 타입스크립트로 프로젝트를 컴파일할 때 자바스크립트 파일도 컴파일 대상에 포함시킬지 선택하는 옵션
    - checkJs: 주로 allowJs 옵션과 같이 사용되며 프로젝트 내 자바스크립트 파일에서 타입스크립트 컴파일 규칙을 적용할지 선택하는 옵션. true를 선택하면 자바스크립트 파일 내부의 에러도 타입스크립트 컴파일 규칙에 따라 검증한 후 에러를 표시한다.
    - noImplicitAny: 타입스크립트는 타입스크립트 코드의 타입을 따로 지정하지 않으면 암묵적으로 모든 타입을 any로 추론한다. 이런 성질을 끄고 켤 수 있는 옵션. true 값을 넣으면 암묵적인 any 타입 추론이 되지 않아 타입을 any로라도 꼭 정의해 주어야 한다. 따라서 타입이 지정되어 있지 않은 자바스크립트 코드 경고를 표시해준다.
 - include: 타입스크립트 컴파일 대상 경로를 지정
```JSON
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,
    "noImplicitAny": false
  },
  "include": ["./src/**/*"]
}

```

---
## 4.3 프로젝트 

### 실습에 사용한 배열 API
 - push(): 배열에 값을 추가할 때 사용하는 API. 배여르이 맨 끝에 값을 추가
 - splice(): 배열 값을 삭제하거나 특정 값을 변경할 때 사용하는 API
 - filter(): 배열에서 특정 조건에 해당하는 값들만 추려 내고 싶을 떄 사용하는 API

<br/>

### 프로젝트 실습

타입스크립트의 역할과 기본 타입, 변수, 함수의 타입 정의 방식을 떠올리며 타입을 정의한다.
 - 타입 표기: 방식을 이용한 타입 정의 방법
 - 변수의 타입 정의 방법
 - 함수의 파라미터 타입과 반환값 타입 정의 방법

<br/>

### 실습 순서

1. ESLint의 에러 표시 부분 타입 정의
2. todoItems 변수 타입 선언
3. todoItems 변수의 타입 선언에 따라 발생하는 에러 코드 정리 및 타입 정의
4. 함수 파라미터나 내부 로직의 타입 정의
5. addTwoTodoItems() 함수 구현
6. 정의한 타입 중에서 좀 더 적절한 타입을 정의할 수 있는 곳이 있는지 확인 및 정의
