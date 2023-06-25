# 15. 타입 호환

## 15.1 타입 호환이란?

타입 호환이란 서로 다른 타입이 2개 있을 때 특정 타입이 다른 타입에 포함되는지를 의미한다.
 - 타입 간 할당 가능 여부로 타입이 호환된다. 혹은 호환되지 않는다라고 표현할 수 있다.
 - string 타입은 모든 문자열이 호환된다.
 - 하지만, 'hi' 라는 문자열 타입은 'hi' 문자열만 호환되고, 다른 문자열을 받지 못한다.
```TS
var a: string = 'hi';
var b: 'hi' = 'hi';

a = b; // ✔ string 타입안에 'hi'가 존재한다. 

var a: string = 'hi';
var b: 'hi' = 'hi';

b = a; // ❌ 'hi' 타입 안에 string 타입이 존재하지 않는다.
```

<br/>

---
## 15.2 다른 언어와 차이점

타입스크립트의 타입 호환은 다른 언어와 차이가 있다.  
 - 타입스크립트는 타입 구조로 호환 여부를 판단하는 구조적 타이핑 특성을 갖는다.
```TS
interface Person {
    name: string;
}

class Human {
    name: string;
}

let i: Person; // Person 타입으로 변수 선언
i = new Human(); // Human 타입으로 객체 생성
```

<br/>

### 15.2.1 구조적 타이핑

구조적 타이핑이란 타입 유형보다는 타입 구조로 호환 여부를 판별하는 언어적 특성을 의미한다.
 - 타입스크립트는 해당 타입이 어떤 타입 구조를 갖고 있는지로 타입 호환 여부를 판별한다.
    - 타입 호환 여부를 판별할 떄는 단순히 특정 타입의 속성 유무만 보지 않고 속성 이름까지 일치하는지 확인한다.
``` TS
type Person {
    name: string;
}

interface Human {
    name: string;
}

var person: Person = {
    name: '사람'
};
var human: Human = {
    name: '인간'
}

human = person;
```

<br/>

---
## 15.3 객체 타입의 호환

객체 타입은 타입 유형에 관계없이 동일한 이름의 속성을 갖고 있고 해당 속성의 타입이 같으면 호환 가능하다.
 - 객체 타입은 인터페이스, 타입 별칭 등 타입 유형이 아니라 최소한의 타입 조건을 만족했는지에 따라 호환 여부가 판별된다.
```TS
type Person = {
    name: string;
};

interface Developer {
    name: string;
    skill: string;
}

var person: Person = {
    name: '홍길동'
};

var developer: Developer = {
    name: '김철수',
    skill: '타입스크립트'
};

person = developer; // ✔ Developer는 name과 skill을 가지고 있다. 때문에, Person 타입의 값을 모두 갖고 있어 문제가 없다.
developer = person; // ❌ Person는 name만 가지고 있다. 때문에, skill이 없어 Developer 타입의 최소 조건을 만족하지 않는다.
```

<br/>

---
## 15.4 함수 타입의 호환

함수를 선언하는 방식에는 함수 선언문(function declaration)과 함수 표현식(function expression)이 있다.  
예제에서는 함수의 타입 호환을 위해함수 표현식으로 정의하였다.  

 - 함수 타입도 구조적 타이핑 관점에서 함수 구조가 유사하면 호환이 된다.
```TS
var add = function(a: number, b: number) {
    return a + b;
}
var sum = function(x: number, y: number) {
    return x + y;
}

add = sum;
sum = add;
```

 - 함수 호환이 되지 않는 경우
    - 함수의 타입 호환은 기존 함수 코드의 동작을 보장해 줄 수 있는가라는 관점으로 볼 수 있다.
    - 특정 함수 타입의 부분 집합에 해당하는 함수는 호환되지만, 더 크거나 타입을 만족하지 못하는 함수는 호환되지 않는다.
        - (x: number, y:number) => number는 (num: number) => number 함수를 호환한다.
        - (num: number) => number는 (x: number, y:number) => number 함수를 호환하지 못한다.
```TS
// 파라미터가 1개인 함수
// (num: number) => number
var getNumber = function(num: number) {
    return num;
}

// 파라미터가 2개인 함수
// (x: number, y:number) => number
var sum = function(x: number, y: number) {
    return x + y;
}

getNumber = sum; // ❌ 컴파일 에러: 파라미터가 2개인 sum 함수가 호환되면, 두 번째 파라미터가 undefined 값이 되어 예상치 못한 결과가 반환된다.
sum = getNumber; // ✔ sum은 기존에 파라미터가 2개였다. 파라미터가 1개인 함수가 호환된다.
```

<br/>

---
## 15.5 이넘 타입의 호환

이넘 타입은 값 여러 개를 하나로 묶어서 사용해야 할 때 활용되는 타입이다.  
이넘 값은 별도의 속성 값을 정의하지 않으면 첫 번째 속성부터 숫자 0 값을 갖고 1씩 증가된다.  

```TS
enum Lanuage {
    C, // 0
    Java, // 1
    Typescript // 2
}
```


<br/>

### 15.5.1 숫자형 이넘과 호환되는 number 타입

숫자형 이넘은 숫자와 호환된다.  

```TS
var a: number = 10;
a = Language.C; // 0
```

<br/>

### 15.5.2 이넘 타입 간 호환 여부

이넘 타입 간에는 구조적 타이핑 개념이 적용되지 않는다.
 - 이넘 타입은 같은 속성과 값을 가졌더라도 이넘 타입 간에는 서로 호환되지 않는다.
```TS
enum Language {
    C,
    Java,
    Typescript
}

enum Programming {
    C,
    Java,
    Typescript
}

var langC: Language.C;
langC = Programming.C; // ❌ 'Programming.C' 형식은 'Language.C' 형식에 할당할 수 없다
```

<br/>

---
## 15.6 제네릭 타입의 호환

제네릭의 타입 호환은 제네릭으로 받은 타입이 해당 타입 구조에서 사용되었는지에 따라 결정된다.
 - 제네릭으로 받은 타입이 해당 타입 구조에서 사용되지 않는다면 타입 호환에 영향을 미치지 않는다.

```TS
interface NotEmpty<T> {
}

var empty1: Empty<string> = '';
var empty2: Empty<number> = 0;

empty1 = empty2; // ✔ 제네릭 타입을 타입 구조에서 사용하지 않아도 호환 가능
empty2 = empty1; // ✔ 제네릭 타입을 타입 구조에서 사용하지 않아도 호환 가능
```

 - 제네릭으로 받은 타입을 해당 타입 구조에서 사용하는 경우 타입 구조를 확인한다.
```TS
interface NotEmpty<T> {
    data: T;
}

var empty1: Empty<string> = '';
var empty2: Empty<number> = 0;

empty1 = empty2; // ❌ NotEmpty<number> 형식은 NotEmpty<string> 형식에 할당할 수 없다.
empty2 = empty1; // ❌ NotEmpty<string> 형식은 NotEmpty<number> 형식에 할당할 수 없다.
```