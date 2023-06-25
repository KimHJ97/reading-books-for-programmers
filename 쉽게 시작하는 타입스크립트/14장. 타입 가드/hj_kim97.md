# 14. 타입 가드

## 14.1 타입 가드란?

타입 가드란 여러 개의 타입으로 지정된 값을 특정 위치에서 원하는 타입으로 구분하는 것을 의미한다.  
타입 시스템 관점에서 넓은 타입에서 좁은 타입으로 타입 범위를 좁힌다라고 볼 수 있다.  

 - 타입 가드를 사용하면 여러 개의 타입 중 하나의 타입으로 걸러낼 수 있다.
```TS
function updateInput(textInput: number | string | boolean) {
    // 타입 가드
    if(typeof textInput === 'number') {
        console.log(textInput); // number 타입이 보장된다.
    }
}
```

<br/>

---
## 14.2 왜 타입 가드가 필요할까?

특정 값이 여러 개의 타입을 받을 수 있다면, 해당 값을 사용하는 시점에 어떤 타입인지를 보장할 수 없다.  
때문에, 특정 타입만의 API 함수를 사용할 수 없다.  
 - number 타입의 toFixed()를 사용하고 싶은데 string 타입일 수도 있다.
 - 타입 단언으로 특정 타입임을 강제할 수 있지만, 실제 실행 시점에 에러를 막을 수 없다.
 - 타입 가드로 특정 타입임을 보장하면, 실제 실행 시점에도 에러가 발생하지 않는다.
```TS
// 타입이 보장이 안된 경우
function updateInput(textInput: number | string) {
    return textInput.toFixed(); // ❌ 'number | string' 형식에 'toFixed' 속성이 없다.
}

// 타입 단언으로 타입 에러 해결하기
function updateInput(textInput: number | string) {
    return (textInput as number).toFixed(); // ✔ textInput이 number 타입임을 강제한다.
}

// 타입 가드로 문제점 해결하기
function updateInput(textInput: number | string) {
    if (typeof textInput === 'number') {
        return textInput.toFixed(); // ✔ textInput이 number 타입임이 보장된다.
    }
    if (typeof textInput === 'string') {
        return textInput.length; // ✔ textInput이 string 타입임이 보장된다.
    }
}
```

<br/>

---
## 14.3 타입 가드 문법

타입 가드에 사용하는 연산자로는 'typeof', 'instanceof', 'in'이 있다.  

<br/>

### 14.3.1 typeof 연산자

typeof는 자바스크립트에 존재하는 연산자로 특정 코드의 타입을 문자열 값으로 변환해준다.  
 - typeof 연산자를 사용하여 특정 위치에서 원하는 타입을 구분할 수 있다.
```TS
typeof 10;              // 'number'
typeof 'hello';         // 'string'
typeof function() {}    // 'function'

function printText(text: string | number) {
    if(typeof text === 'string') {
        console.log(text.trim());
    }

    if(typeof text === 'number') {
        console.log(text.toFixed());
    }
}
```

<br/>

### 14.3.2 instanceof 연산자

instanceof는 자바스크립트에 존재하는 연산자로 변수가 대상 객체의 프로토타입 체인에 포함되는지 확인하여 true/false를 반환해준다.  
 - 모든 객체는 기본적으로 Object를 프로토타입으로 상속받는다.
 - instanceof는 주로 클래스 타입이 유니언 타입으로 묶여 있을 때 타입을 구분하기 위해 사용된다.
```TS
class Person {
    name: string;
    age: number;

    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
}

var person = new Person('로그', 20); // person -> Person -> Object
person instanceof Person; // true

var hulk = { name: '헐크', age: 21 }; // hulk -> Object
hulk instanceof Person; // false

function fetchInfoByProfile(profile: Person | string) {
    if(profile instanceof Person) {
        // profile의 타입이 Person으로 보장된다.
        ..
    }
}
```

<br/>

### 14.3.3 in 연산자

in 연산자는 자바스크립트에 존재하는 연산자로 객체에 속성이 있는지 확인해준다.  
객체에 특정 속성이 있으면 true, 그렇지 않으면 false를 반환해준다.  

```TS
var book = {
    name: '쉽게 시작하는 타입스크립트',
    rank: 1
};

console.log('name' in book); // true
console.log('address' in book); // false

interface Book {
    name: string;
    rank: number;
}

interface OnlineLecture {
    name: string;
    url: string;
}

function learnCourse(material: Book | OnlineLecture) {
    if('rank' in material) {
        // material의 타입이 Book 타입으로 간주된다.
    }

    if('url' in material) {
        // material의 타입이 OnlineLecture 타입으로 간주된다.
    }
}
```

<br/>

---
## 14.4 타입 가드 함수

타입 가드 함수란 타입 가드 역할을 하는 함수를 의미한다.  
주로 객체 유니언 타입 중 하나를 구분하는 데 사용하며, in 연산자와 역할은 같지만 좀 더 복잡한 경우에도 사용할 수 있다.  

<br/>

### 14.4.1 타입 가드 함수 예시

```TS
interface Person {
    name: string;
    age: number;
}

interface Developer {
    name: string;
    skill: string;
}

function isPerson(someone: Person | Developer): someone is Person {
    return (someone as Person).age !== undefined;
}

function greet(someone: Person | Developer) {
    if(isPerson(someone)) {
        console.log(`사람의 나이는 ${someone.age}`);
    } else {
        console.log(`개발자의 스킬은 ${someone.skill}`);
    }
}
```

<br/>

---
## 14.5 구별된 유니언 타입

구별된 유니언 타입이란 유니언 타입을 구성하는 여러 개의 타입을 특정 속성의 유무가 아니라 특정 속성 값으로 구분하는 타입 가드 문법을 의미한다.  
 - 여러 개의 타입중에 공통 속성이 있고, 그 속성의 값으로 구분하는 것
 - 속성 유무가 아니라 속성의 문자열 타입 값을 비교해서타입을 구분하는 것
```TS
interface Person {
    name: string;
    age: number;
    industry: 'common';
}

interface Developer {
    name: string;
    age: string;
    industry: 'tech'
}

function greet(someone: Person | Developer) {
    if(someone.industry === 'common') {
        // someone의 타입이 Person으로 타입 추론
    }
        if(someone.industry === 'tech') {
        // someone의 타입이 Developer으로 타입 추론
    }
}
```
