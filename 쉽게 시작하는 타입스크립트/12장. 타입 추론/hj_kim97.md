# 12. 타입 추론

## 12.1 타입 추론이란?

타입 추론은 타입스크립트가 코드를 해석하여 적절한 타입을 정의하는 동작을 의미한다.  
변수를 선언하고 값을 할당하면 해당 변수의 타입이 자동으로 추론된다.
 - 변수를 초기화하거나 함수의 파라미터에 기본값을 설정하거나 반환값을 설정했을 때 지정된 값을 기반으로 적당한 타입을 제시하고 정의해 주는 것

```TS
var a = 10; // number 타입 추론
```

<br/>

---
## 12.2 변수의 타입 추론 과정

변수에 값을 할당하지 않고 선언만 하면 any 타입으로 추론된다.  
이렇게 변수 선언 시점에 어떤 값이 들어올지 모르는 경우 어떤 값이든 받을 수 있는 any 타입으로 추론된다.  
 - 변수를 선언할 때 할당된 초깃값에 따라서 적절한 타입이 추론된다.
    - 만약, 변수를 선언한 이후에 값을 변경하더라도 그 값으로 타입이 변경되지는 않는다.
 - 초깃값이 없는 경우 any 타입 추론
 - 초깃값을 문자열로하면 string 타입 추론
```TS
var a; // any 타입 추론
a = 10; // any 타입
var b = 'hello'; // string 타입 추론
```

<br/>

---
## 12.3 함수의 타입 추론: 반환 타입

함수를 호출하여 반환된 결과 값을 변수에 할당하면 반환된 결과 값에 따른 타입으로 추론된다.  
함수의 파라미터 타입과 내부 로직으로 반환 타입이 자동으로 추론된다.

```TS
// 반환 타입이 제거된 함수: number 타입 반환
function sum(a: number, b: number) {
    return a + b;
}
// 반환 타입이 제거된 함수: boolean 타입 반환
function isNumberEquals(a: number, b: number) {
    return a == b;
}

var result = sum(1, 2); // number 타입 추론
var result2 = isNumberEquals(1, 2); // boolean 타입 추론
```

<br/>

---
## 12.4 함수의 타입 추론: 파라미터 타입

```TS
// 파라미터에 기본 값 지정
function getA(a = 10) {
    return a;
}
function getString(a = 10) {
    return a + "";
}

var result = getA(); // number 타입 추론
var result2 = getString(); // string 타입 추론: number + string은 자동으로 string 타입이 된다.
```

<br/>

---
## 12.5 인터페이스와 제네릭의 추론 방식

인터페이스에 제네릭을 사용할 때에도 타입스크립트 내부적으로 적절한 타입을 추론해준다.

```TS
interface Dropdown<T> {
    title: string;
    value: T;
}

let shoppingItem: Dropdown<number>; // Dropdown { title: string; value: number } 타입 추론
```

<br/>

---
## 12.6 복잡한 구조에서 타입 추론 방식



```TS
interface Dropdown<T> {
    title: string;
    value: T;
}

interface DetailedDropdown<K> extends Dropdown<K> {
    tag: string;
    description: string;
}

let shoppingDetailItem: DetailedDropdown<number>;
```
 - shoppingDetailItem이 아래처럼 타입 추론이 된다.
    - DetailedDropdown 인터페이스에 넘긴 제네릭 타입이 Dropdown 인터페이스의 제네릭 타입으로 전달되었다.
    - DetailedDropdown 인터페이스 내부에서는 제네릭으로 받은 타입을 사용하지 않고, 부모인 Dropdown 인터페이스의 제네릭 타입으로 넘겨주는 역할을 한다.
```TS
interface DetailedDropdown {
    tag: string;
    description: string;
    title: string;
    value: number;
}

shoppingDetailItem = {
    title: '쉽게 시작하는 타입스크립트',
    description: '믿고 보는 캡틴판교의 타입스크립트 입문서',
    tag: '타입스크립트',
    value: 1
}
```