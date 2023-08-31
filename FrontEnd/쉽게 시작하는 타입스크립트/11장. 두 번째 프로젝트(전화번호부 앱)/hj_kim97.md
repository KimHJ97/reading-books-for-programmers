# 11. 두 번째 프로젝트: 전화번호부 앱

## 11.1 프로젝트 환경 구성

링크를 통해 프로젝트를 받는다.  
할 일 관리 앱은 '2_address-book' 폴더의 프로젝트를 사용한다.  
해당 폴더에 접근 후 'npm i'로 package.json의 설정된 내용으로 의존성 모듈들을 설치한다.
 - [프로젝트 코드 링크](https://github.com/joshua1988/learn-typescript)
 - [프로젝트 코드 링크](https://github.com/gitbutITbook/080316)

<br/>

---
## 11.2 프로젝트 폴더 구조

<p align="center">
  <img src="./images/%ED%8F%B4%EB%8D%94%EA%B5%AC%EC%A1%B0.PNG" alt="프로젝트 구조" />
</p>

<br/>

### 11.2.1 node_modules 폴더

node_modules 폴더에는 실습에 필요한 라이브러리가 설치된다.  
npm i 명령어를 입력해서 필요한 라이브러리를 설치하는데, 정상적으로 설치가 종료되면 node_modules 폴더가 생성된다.

<br/>

### 11.2.2 src 폴더

프로젝트 실습에 필요한 소스 파일이 있는 폴더로 index.ts 파일이 존재한다.

<br/>

### 11.2.3 .eslintrc.js

자바스크립트 확장자로 작성된 ESLint 설정 파일이다.  
ESLint는 자바스크립트의 코드 규칙을 검사할 뿐만 아니라 타입스크립트의 린트 규칙을 추가하여 타입스크립트 코드도 검사할 수 있다.

<br/>

### 11.2.4 package.json, package-lock.json 파일

package.json 파일은 프로젝트 관련 정보가 담겨 있는 NPM 설정 파일이다.  
프로젝트 이름, 버전, 라이선스뿐만 아니라 프로젝트 실행에 필요한 라이브러리 목록도 지정되어 있다.  
package-lock.json 파일은 NPM 설치 명령어로 필요한 라이브러리를 설치할 때 생성 및 변경되는 파일이다.  
설치하는 라이브러리 간 버전을 관리하는데, NPM에서 내부적으로 관리하는 파일로 직접 수정할 일은 없다.

<br/>

### 11.2.5 tsconfig.json 파일

tsconfig.json 파일은 타입스크립트 관련 설정이 담겨 있는 타입스크립트 설정 파일이다.

 - compilerOptions: 타입스크립트 컴파일과 관련된 옵션을 지정할 수 있다.
    - allowJs: 타입스크립트 컴파일 대상에 자바스크립트도 포함할지 정한다.
    - checkJs: 프로젝트 내 자바스크립트 파일에 타입스크립트 컴파일 규칙을 적용할지 정한다.
    - noImplicitAny: 타입이 지정되어 있지 않으면 암묵적 any로 간주할지 설정한다.
    - target: 타입스크립트 코드가 자바스크립트 코드로 컴파일되었을 때 자바스크립트 코드가 실행될 환경을 지정한다. 기본값은 es3이다.
    - lib: 자바스크립트 기본 문법이나 브라우저 API 등 자주 사용되는 문법에 대해 작성된 타입스크립트 선언 파일의 사용 여부를 정하는 옵션이다.
```JSON
{
  "compilerOptions": {
    "allowJs": true,
    "checkJs": true,
    "target": "es5",
    "lib": ["es2015", "dom", "dom.iterable"],
    "noImplicitAny": false
  },
  "include": ["./src/**/*"]
}
```

<br/>

## 11.3 프로젝트 로직

 - Contact 인터페이스
    - 이름, 주소, 전화번호 목록
 - PhoneNumberDictionary 인터페이스
    - 전화번호
 - fetchContacts() 함수
    - 서버에 데이터를 요청하는 API 함수를 모방하였다.
    - 2초 후 contacts 변수에 담긴 배열이 반환된다.
 - AddressBook 클래스
    - contacts 속성: 전화번호부 목록
    - findContactByName(name): 입력받은 이름으로 연락처를 찾는 메서드
    - findContactByAddress(address): 주소로 연락처를 찾는 메서드
    - findContactByPhone(phoneNumber, phoneType): 전화번호와 번호 유형으로 연락처를 찾는 메서드
    - addContact(contact): 새 연락처를 전화번호부에 추가하는 메서드
    - displayListByName(): 전화번호부 목록의 이름만 추출해서 화면에 표시하는 메서드
    - displayListByAddress(): 전화번호부 목록의 주소를 화면에 표시하는 메서드

## 11.4 프로젝트 실습

 - 1. 타입스크립트 설정 파일의 noImplicitAny 속성 값을 true로 변경  
    - 변수나 함수의 파라미터 타입이 정의되어 있지 않아 발생하는 타입 에러가 표시된다.
 - 2. 타입스크립트 설정 파일의 strict 속성 값을 true로 변경
 - 3. ESLint 설정 파일의 @typescript-eslint 관련 규칙 2개 모두 주석처리
    - 함수의 반환 타입이 지정되어 있지 않거나 타입이 지정되어야 할 곳에 타입이 없으면 ESLint 에러가 표시된다.
