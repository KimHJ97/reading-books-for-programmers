# 2. 타입스크립트 시작하기

## 2.1 타입스크립트 학습을 위한 개발 환경 설정
타입스크립트 개발 환경을 구성하기 위해서는 세 가지가 준비되어야 한다.
 - 크롬 브라우저
 - Node.js와 NPM
 - 비주얼 스튜디오 코드(VSCode)

### 2.1.1 크롬 브라우저 설치

크롬(Chrome) 브라우저는 구글이 개발한 웹 브라우저이다.  
실습을 진행한 후에 크람 브라우저나 Node.js 환경에서 결과를 확인할 수 있으므로 구글에서 크롬 브라우저를 검색하여 내려받을 수 있다.

### 2.1.2 Node.js와 NPM 설치

Node.js는 자바스크립트를 실행할 수 있는 실행 환경이다.  
Node.js를 설치하면 NPM이 함께 설치되는데, NPM이 있어야 타입스크립트를 명령어로 설치할 수 있다.  
 - [Node.js 공식 사이트](https://nodejs.org/ko/)
 - LTS는 안정화 버전으로, 사용할 수 있는 Node.js의 기능들이 안정화되어 있다는 의미이다.

```sh
# 설치된 버전 확인
$ node -v
$ npm -v
```

### 2.1.3 비주얼 스튜디오 코드 설치

비주얼 스튜디오 코드는 마이크로소프트에서 제작한 무료 텍스트 에디터이다.  
2023년도에 프론트엔드 개발자들에게 가장 인기 있는 개발 도구이며 타입스크립트로 개발되었다.  
타입스크립트 언어를 제작한 회사이기도하여 타입스크립트와 호환성이 좋다.  
 - [VScode 공식 사이트](https://code.visualstudio.com/)

### 2.1.4 비주얼 스튜디오 코드 테마와 플러그인 설치

테마란 비주얼 스튜디오 코드의 외관을 꾸밀 수 있는 기능이고, 플러그인은 개발할 때 유용한 기능을 제공하는 확장 프로그램이다.
 - GitHub Plus Theme
   - 해당 플러그인은 비주얼 스튜디오 코드의 다양한 테마 플러그인 중 하나이다.
        - 설치 후 'ctrl + shit + p'를 눌러 명령어 팔레트창을 실행한다.
        - 팔레트창에서 설치한 테마 플러그인을 적용하기 위해 'color theme'를 검색한다.
        - GitHub Plus를 선택한다.
 - ESLint
    - ESLint는 자바스크립트 문법 검사 도구이다.
        - 설치 후 '파일' > '기본 설정' > '설정 메뉴'로 진입한다.
        - '설정 검색'에서 'eslint dire'를 검색하고, 'settings.json에서 편집' 링크 클릭한다.
        - 'settings.json' 파일의 아래 옵션을 수정하여 ESLint 설정이 인식되도록 한다.
        ```
        "eslint.workingDirectories": [{"mode": "auto"}]
        ```
 - Korean Language Pack For Visual Code: 비주얼 스튜디오 코드 한국어 확장 팩
 - JavaScript (ES6) code snippets: 최신 자바스크립트 문법 작성 보조 도구
 - Live Server: 로컬 서버 실행 도구
 - Night Owl: 밤 올빼미 테마
 - Material Icon Theme: 파일 확장자에 따라 폴더 이미지를 예쁘게 표시하는 아이콘 테마
 - Path Intellisense: 파일 경로 자동 완성 보조 도구
 - TODO Highlight: TODO, FIXME 등 문구를 강조해 주는 플러그인

<center>
    <img src="./images/ESLint_%EC%84%A4%EC%A0%95.PNG" alt="ESLint 설정" />
</center>

---
## 2.2 타입스크립트 프로젝트 시작

### NPM 설정 파일 및 타입스크립트 설치하기

현재 브라우저에서 타입스크립트 파일을 인식할 수 없기 떄문에, 타입스크립트 파일을 실행하려면 자바스크립트 파일로 변환해 주어야 한다.  
타입스크립트 프로젝트는 타입스크립트를 자바스크립트로 변환하는 라이브러리와 빌드 도구를 갖는다.  
 - 1. 타입스크립트 소스 코드를 작성한다.
```JS
// index.ts: 타입스크립트 소스 코드 작성(확장자: *.ts)
function sum(a: number, b: number) {
    return a + b;
}
```
 - 2. 타입스크립트 프로젝트를 생성한다.
```Shell
# 1. 프로젝트 생성
# npm init -y는 NPM 설정 파일을 기본값으로 생성하는 명령어이다.
# 최신 프론트엔드 프레임워크를 사용하는 프로젝트는 대부분 NPM 기반으로 관리된다.
$ npm init -y

# 2. 타입스크립트 NPM 패키지 설치
$ npm install typescript -D
```
 - 3. 타입스크립트 소스 코드를 컴파일한다.
```Shell
# tsc는 타입스크립트 컴파일러(TypeScript Compiler)를 의미한다.
# index.ts 파일이 index.js 파일로 컴파일된다.
$ node ./node_modules/typescript/bin/tsc index.ts
```
