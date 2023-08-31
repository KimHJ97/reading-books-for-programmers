# 10. 제네릭

## 10.1 제네릭이란?

제네릭은 타입을 미리 정의하지 않고 사용하는 시점에 원하는 타입을 저의해서 쓸 수 있는 문법이다.  
마치 함수의 파라미터와 같은 역할을 하는데, 함수의 인자에 넘긴 값을 함수의 파라미터로 받아 함수 내부에서 그대로 사용하는 방식과 비슷하다.  
제네릭은 타입을 인자로 넘기고, 그 타입을 그대로 사용하는 것으로 볼 수 있다.

<br/>

---
## 10.2 제네릭 기본 문법

 - 함수를 정의할 때 함수명 옆에 <T>를 정의한다.
    - 함수를 호출하는 곳에서 <T>에 대한 타입을 정의한다.
    - 함수에서 사용된 T는 넘겨받은 타입으로 변환되어 사용된다.
```TS
function getText<T>(text: T): T {
    return text;
}

getText<string>('hi'); // hi
getText<number>(100); // 100
```

<br/>

---
## 10.3 왜 제네릭을 사용할까?

### 10.3.1 중복되는 타입 코드의 문제점

타입을 미리 정의하지 않고 호출할 때 타입을 정의해서 사용하는 이유는 반복되는 타입 코드를 줄여 주기 때문이다.  
다양한 타입으로 동일한 기능을 수행하는 함수를 사용하고 싶다면, 다양한 타입을 받는 다른 이름의 함수를 정의해야 한다.  
이러한 문제를 any 타입을 이용하여 해결할 수 있지만, 타입스크립트의 장점이 사라지게 된다.  

```TS
function getText(text: string): string {
    return text;
}
function getNumber(text: number): number {
    return number;
}

// any 타입 이용
function getText(text: any): any {
    return any;
}
```

### 10.3.2 제네릭으로 해결되는 문제점

```TS
function getText<T>(text: T): T {
    return text;
}

var myString = getText<string>('hi'); // ✔ myString이 string 타입으로 추론된다.
myString.toString();

var myNumber = getText<number>(100); // ✔ myNumber가 number 타입으로 추론된다.
myNumber.toFixed();
```

<br/>

---
## 10.4 인터페이스에 제네릭 사용하기

제네릭은 함수뿐만 아니라 인터페이스에도 사용할 수 있다.

 - 상품 목록과 상품의 재고, 주소를 보여주는 드롭다운 UI를 인터페이스로 정의한다고 가정한다.
    - 제네릭을 사용하지 않는 경우
        - 새로운 인터페이스가 생길때마다 모든 데이터 타입을 일일이 정의해야한다.
    - 제네릭을 사용하는 경우
        - Dropdown 인터페이스를 생성하고, 제네릭 타입을 사용한다.
```TS
interface ProductDropdown {
    value: string;
    selected: boolean;
}

interface StockDropdown {
    value: number;
    selected: boolean;
}

interface AddressDropdown {
    value: { city: string; zipCode: string };
    selected: boolean;
}

// 드롭다운 유형별로 각각의 인터페이스 연결
var product: ProductDropdown;
var stock: StockDropdown;
var address: AddressDropdown;

// 제네릭 사용
interface Dropdown<T> {
    value: T;
    selected: boolean;
}

// 드롭다운 유형별로 하나의 제네릭 인터페이스 연결
var product: Dropdown<string>;
var stock: Dropdown<number>;
var address: Dropdown<{ city: string; zipCode: string }>;
```

<br/>

---
## 10.5 제네릭의 타입 제약

제네릭의 타입 제약은 제네릭으로 타입을 정의할 떄 좀 더 정확한 타입을 정의할 수 있게 도와주는 문법이다.  
extends, keyof 등 키워드를 사용하여 타입을 제약할 수 있다.

<br/>

### 10.5.1 extends를 사용한 타입 제약

제네릭의 장점은 타입을 미리 정의하지 않고 호출하는 시점에 타입을 정의해서 유연하게 확장할 수 있다는 점이다.  
유연하게 확장한다는 것은 타입을 별도로 제약하지 않고 아무 타입이나 받아서 쓸 수 있다는 의미이다.  
즉, string, number, boolean, object, any 등 모든 타입을 받을 수 있다.  
때문에, 모든 타입이 아니라 몇 개의 타입만 제네릭으로 받고 싶을 때 타입 제약을 이용할 수 있다.  

 - 제네릭을 선언하는 부분에 <T extends 타입>과 같은 형태로 타입을 제약할 수 있다.
```TS
// 타입 제약 X
function embraceEverything<T>(thing: T): T {
    return thing;
}
embraceEverything<string>('hi');
embraceEverything<number>(100);
embraceEverything<boolean>(false);
embraceEverything<{ name: string }>({ name: 'log' });
embraceEverything<any>(100);

// extends 타입 제약
// length 속성을 갖는 타입만 취급하도록 하는 예제 코드이다.
// length 속성을 갖는 타입은 string, array, object가 있다.
function lengthOnly<T extends { length: number }>(value: T) {
    return value.length;
}

lengthOnly('hi');
lengthOnly([1, 2, 3]);
lengthOnly({ title: 'abc', length: 123 });
```

### 10.5.3 keyof를 사용한 타입 제약

keyof는 특정 타입의 키 값을 추출해서 문자열 유니언 타입으로 변환해준다.  

```TS
// keyof 연산자
type DeveloperKeys = keyof { name: string; skill: string; } // type DeveloperKeys = "name" | "skill"

// 제네릭 타입에 keyof 연산자 사용
// extends와 keyof를 조합해서 name과 skill 속성을 갖는 객체의 키만 타입으로 받겠다고 정의한다.
function printKeys<T extends keyof { name: string; skill: string; }>(value: T) {
    console.log(value);
}

printKeys('address'); // ❌ '"address"' 형식의 인수는 '"name" | "skill"' 형식의 매개 변수에 할당될 수 없다.
printKeys('name'); // ✔ '"name"' 형식의 인수는 '"name" | "skill"' 둘 중 하나에 해당된다.
```