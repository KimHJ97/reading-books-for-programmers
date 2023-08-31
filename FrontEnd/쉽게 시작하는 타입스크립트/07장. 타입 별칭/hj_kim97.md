# 7. 타입 별칭

<br/>

## 7.1 타입 별칭이란?

타입 별칭은 특정 타입이나 인터페이스 등을 참조할 수 있는 타입 변수를 의미한다.  
쉽게, 타입에 의미를 부여해서 별도의 별칭을 주는 것이다.  
여러 번 반복되는 타입을 변수화해서 쉽게 표기하고 싶을 때 사용할 수 있다.

```TS
type MyName = string;
const name1: MyName = "철수";
const name2: string = "영희";

type MyMessage = string | number;
function printText(text: MyMessage) {
    console.log(text);
}
const message: MyMessage = 'Hello';
printText(message);
```

<br/>

---
## 7.2 타입 별칭과 인터페이스의 차이점

타입 별칭과 인터페이스 모두 객체 타입을 정의할 수 있다.  
또한, 여러 번 반복되는 타입을 타입 별칭 혹은 인터페이스를 이용하여 쉽게 표기할 수 있다.  
둘의 사용 방법과 기능이 비슷하여 햇갈릴 수 있다.

```TS
type Person = {
    id: string;
    number: string;
}

interface Person = {
    id: string;
    name: string;
}
```

<br/>

### 7.2.1 사용할 수 있는 타입의 차이

타입 별칭과 인터페이스를 구분 짓는 차이점은 정의할 수 있는 타입 종류에 있다.  
인터페이스는 주로 객체의 타입을 정의하는 데 사용하는 반면, 타입 별칭은 일반 타입에 이름을 짓는 데 사용하거나 유니언 타입, 인터섹션 타입 등에도 사용할 수 있다.  
반대로 이런 타입들은 인터페이스로는 정의할 수 없다.  
또한 타입 별칭은 제네릭이나 유틸리티 타입 등 다양한 타입에 사용할 수 있다.

```TS
// 타입 별칭
type ID = string;
type Product = TShirt | Shoes;
type Teacher = Person & Adult;

type Gilbut<T> = {
    book: T;
}

type MyBeer = Pick<Beer, 'brand'>;

// 인터페이스와 타입 별칭
interface Person {
    name: string;
    age: number;
}

type Adult = {
    old: boolean;
}

type Teacher = Person & Adult;
```

<br/>

### 7.2.2 타입 확장 관점에서 차이

타입 확장이란 이미 정의되어 있는 타입들을 조합해서 더 큰 의미의 타입을 생성하는 것을 의미한다.  
타입 별칭과 인터페이스의 타입 확장하는 방식이 다르다.  

 - 인터페이스
    - 인터페이스는 타입을 확장할 때 상속이라는 개념을 이용한다.
    - extends 키워드를 사용해서 부모 인터페이스의 타입을 자식 인터페이스에 상속해서 사용한다.
```TS
interface Person {
    name: string;
    age: number;
}

interface Developer extends Person {
    skill: string;
}

const log: Developer = {
    name: '로그',
    age: 20,
    skill: 'Typescript'
};
```
 - 타입 별칭
    - 타입 별칭은 인터섹션 타입으로 객체 타입을 2개 합쳐서 사용할 수 있다.
    - & 연산자를 사용한 인터섹션 타입으로 합친다.
```TS
type Person = {
    name: string;
    age: number;
}

type Developer = {
    skill: string;
}

// ✔ 인터섹션 타입을 별도의 타입 별칭으로 정의할 수도 있다.
type DeveloperPerson = Person & Developer;

const log: Person & Developer = {
    name: '로그',
    age: 20,
    skill: 'Typescript'
}
```

<br/>

### 7.2.3 인터페이스 선언 병합

작성된 타입을 어떻게 조합하느냐에 따라 인터페이스를 쓰거나 타입 별칭을 사용할 수 있다.  
추가적으로 인터페이스에는 동일한 이름으로 인터페이스를 선언하면 인터페이스 내용을 합치는 특성이 있는데 이를 선언 병합이라고 한다.  

```TS
interface Person {
    name: string;
    age: number;
}

interface Person {
    skill: string;
}

const log: Person = {
    name: '로그',
    age: 20,
    skill: 'Typescript'
}
```

<br/>

---
## 7.3 타입 별칭은 언제 쓰는 것이 좋을까?

인터페이스와 타입 별칭 모두 반복되는 타입에 대해서 쉽게 사용할 수 있는 기능을 제공한다.  
때문에, 어떤 상황에서 인터페이스를 써야되고, 어떤 상황에서 타입 별칭을 사용해야 하는지에 대한 의문이 생긴다.  
2021년 이전에는 타입스크립트 공식 문서에 '좋은 소프트웨어는 확장이 용이해야 한다'라는 관점에서 타입 별칭보다 인터페이스를 사용하기를 권장했다.  
하지만, 현재 공식사이트에서 해당 문구가 사라지고 커뮤니티에서는 인터페이스와 타입 별칭이 개인 선호에 따라 사용이 권장되기도 한다.  
 - 따로 언제 사용해야 한다고 정해진 것은 없지만, 아래 정의처럼 상황에 따라 사용하는 것으로 일관성을 유지하는 것이 좋다.
    - 타입 별칭으로만 타입 정의가 가능한 곳에서는 타입 별칭을 사용
    - 백엔드와의 인터페이스를 정의하는 곳에서는 인터페이스를 사용

<br/>

### 7.3.1 타입 별칭으로만 정의할 수 있는 타입

인터페이스가 아닌 타입 별칭으로만 정의할 수 있는 타입은 주요 데이터나 타입이나 인터섹션, 유니언 타입이다.  
인터페이스는 객체 타입을 저의할 때 사용하는 타입으로 아래의 타입은 인터페이스로 정의할 수 없다.  
또한, 제네릭, 유틸리티 타입, 맵드 타입과도 연동하여 사용할 수 있다.

```TS
type MyString = string;
type StringOrNumber = string | number;
type Admin = Person & Developer;

// 제네릭
// 제네릭은 인터페이스와 타입 별칭 모두 사용 가능하다.
type Dropdown<T> = {
    id: string;
    title: T;
}

// 유틸리티 타입: 기존에 정의된 타입을 변경하거나 일부만 활용할 때 사용한다.
type Admin = { name: string; age: number; role: string; }
type OnlyName = Pick<Admin, 'name'>

// 맵드 타입
type Picker<T, K extends keyof T> = {
    [P in K]: T[P];
};
```

<br/>

### 7.3.2 백엔드와의 인터페이스 정의

웹 서비스를 프론트엔드와 백엔드로 역할을 나누어 개발할 때 백엔드에서 프론트엔드로 어떻게 데이터를 넘길지 정의하는 작업이 필요하다.  
이러한 작업을 인터페이스를 정의한다고 표현한다.  

 - 인터페이스를 이용하면 상속과 선언 병합을 이용하여 유연하게 타입을 확장할 수 있다.
    - 서비스 요구 사항이 변경되거나, 개발 단계에서는 데이터 구조가 자주 바뀌게 된다.
```TS
interface Admin {
    role: string;
    department: string;
}

// 상속을 통한 인터페이스 확장
interface User extends Admin {
    id: string;
    name: string;
}

// 선언 병합을 통한 타입 확장
interface User {
    skill: string;
}

const log: User = {
    id: 'log',
    name: '로그',
    role: 'ADMIN',
    department: 'Development Team',
    skill: 'Typescript'
}
```

