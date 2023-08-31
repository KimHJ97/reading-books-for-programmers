# 3. 타입스크립트 기초(변수와 함수의 타입 정의)

## 3.1 변수에 타입을 정의하는 방법

변수에 타입을 선언하고 싶다면 변수 뒤에 ': 타입이름'을 추가하면 된다.  
여기서, 콜론(:)을 타입 표기(type annotation)라고 한다.  
타입 표기는 변수뿐만 아니라 함수에도 사용할 수 있다.  
```TS
const name: string = 'log';
```

<br/>

---
## 3.2 기본 타입

변수나 함수의 타입을 정의할 때 사용할 수 있는 타입 종류는 여러 가지가 있다.  
 - string
 - number
 - boolean
 - object
 - Array
 - tuple
 - any
 - null
 - undefined

<br/>

### 3.2.1 문자열 타입: string

string은 문자열을 의미하는 타입이다.
문자열이 아닌 다른 값을 할당하면 타입 에러가 표시된다.
```TS
const name: string = 'log';
```
<p align="center">타입에러 예시</p>
<p align="center">
  <img src="./images/%ED%83%80%EC%9E%85%EC%97%90%EB%9F%AC.PNG" alt="JSDoc_사용안했을때" />
</p>

<br/>

### 3.2.2 숫자 타입: number

특정 변수가 숫자만 취급하면 number 타입을 사용한다.
```TS
const age: number = 100;
```

<br/>

### 3.2.3 진위 타입: boolean

진위 값만 취급하는 변수에는 boolean 타입을 사용한다.  
참과 거짓을 구분하는 진위 값을 다룰 때 사용한다.
```TS
const isLogin: boolean = false;
```

<br/>

### 3.2.4 객체 타입: object

객체 유형의 데이터를 취급할 때는 object를 사용한다.
```TS
const person: object = {
    name: 'log',
    age: 100
};
```

<br/>

### 3.2.5 배열 타입: Array

배열 타입을 정의할 때는 'Array<자료형>', '자료형[]'을 이용한다.  
배열 타입을 선언할 때 Array<string> 보다 string[] 형태의 문법 사용을 권장한다.  
이 2개는 문법적으로만 다를 뿐 역할은 완전 동일하다.
```TS
// 문자열 배열
var companies: Array<string> = ['네이버', '삼성', '인프런'];
var companies: string[] = ['네이버', '삼성', '인프런'];

// 숫자 배열
var cards: Array<number> = [1, 2, 3, 4];
var cards: number[] = [1, 2, 3, 4];
```

<br/>

### 3.2.6 튜플 타입: tuple

튜플은 특정 형태를 갖는 배열을 의미한다.  
배열 길이가 고정되고 각 요소 타입이 정의된 배열을 튜플이라고 한다.
 - 정해진 순서와 타입에 맞지 않는 값이 취급되면 에러가 발생한다.

```TS
var items: [string, number] = ['hi', 100];
var items: [string, number] = ['hi', 'hello']; // ❌ 컴파일 에러
```

<br/>

### 3.2.7 any

any 타입은 아무 데이터나 취급한다는 의미이다.  
타입스크립트에서 자바스크립트의 유연함을 취할 때 사용되는 타입이다.
```TS
var myName: any = 'log';
myName = 100;
```

### 3.2.8 null과 undefined

자바스크립트에서 null은 의도적인 빈 값을 의미한다.  
반면 undefined는 변수를 선언할 때 값을 할당하지 않으면 기본적으로 할당되는 초깃값이다.
```TS
// null 타입 지정하고, null 값 할당
var empty: null = null;
// undefined 지정하고, 아무 값도 할당하지 않음 (초깃값 undefined)
var nothingAssigned: undefined;
```

<br/>

---
## 3.3 함수에 타입을 정의하는 방법

함수는 자주 사용되는 문법으로 반복되는 코드를 줄이는 방법이자 데이터를 전달 및 가공하는 데 사용된다.  

<br/>

### 3.3.1 JavaScript 함수

'function' 이라는 예악어와 함수 이름으로 함수를 선언할 수 있고, 함수 본문에 'return'을 추가해서 값을 반환하거나 함수 실해을 종료할 수 있다.
 - 예약어: 프로그래밍 언어에 미리 정의된 단어로 '키워드'라고도 한다.

```JS
function sayWord(word) { // 함수의 파라미터 word를 매개변수라고 한다.
    return word;
}
sayWord('hello'); // 넘긴 문자열 'hello'를 인자라고 한다.
```

<br/>

### 3.3.2 함수의 타입 정의: 파라미터와 반환값

함수의 타입을 정의할 때는 먼저 입력 값과 출력 값에 대한 타입을 정의한다.
 - 함수의 반환값 타입은 함수 이름 오른쪽에 ': 자료형'으로 지정한다.
 - 함수의 입력값인 파라미터로 타입을 지정할 수 있다.

```TS
function sayWord(word: string): string {
    return word;
}
```

<br/>

---
## 3.4 타입스크립트 함수 인자 특징

자바스크립트 함수에서는 파라미터와 인자의 개수가 일치하지 않아도 프로그래밍상에서 문제가 없었다.  
하지만, 타입스크립트에서는 파라미터와 인자의 개수가 다르면 에러가 발생한다.

```JS
// JavaScript에서는 파라미터의 숫자보다 인자의 개수가 많더라도 에러가 발생하지 않는다.
function sayWord(word) {
    return word;
}
sayWord('hi', 'hello'); // ✔ 정상 동작 hi
```
```TS
function sayWord(word) {
    return word;
}
sayWord('hi', 'hello'); // ❌ 컴파일 에러
```

<br/>

---
## 3.5 옵셔널 파라미터

파라미터의 개수를 선택적으로 받고 싶은 경우가 있다.  
이때, 옵셔널 파라미터 기능을 사용할 수 있다.
 - 옵셔널 파라미터를 ?로 표기한다.
 - 파라미터에 ?가 붙으면 옵셔널 파라미터로 정의되며, 호출할 떄 넘겨도 되고 넘기지 않아도 된다.

```TS
function sayMyName(firstName: string, lastName?: string): string {
    return 'My Name: ' + firstName + ' ' + lastName;
}
sayMyName('log'); // ✔ My Name: log
```
