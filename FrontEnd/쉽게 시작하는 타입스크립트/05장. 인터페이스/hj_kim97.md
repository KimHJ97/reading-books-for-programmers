# 5. 인터페이스

## 5.1 인터페이스란?

타입스크립트에서 인터페이스는 객체 타입을 정의할 때 사용하는 문법이다.  
 - 객체의 속성과 속성 타입
 - 함수의 파라미터와 반환 타입
 - 함수의 스팩(파라미터 개수와 반환값 여부 등)
 - 배열과 객체를 접근하는 방식
 - 클래스

<br/>

---
## 5.2 인터페이스를 이용한 객체 타입 정의

인터페이스는 객체의 타입을 정의할 때 사용한다.
 - 인터페이스의 타입과 맞지 않는 객체에 인터페이스를 지정하면 에러가 발생한다.
```TS
interface Person {
    name: string;
    age: number;
}

const log: Person = { name: '로그', age: 20 }; // ✔ 정상
const log2: Person = { name: '로그', age: '20' }; // ❌ 'string' 형식은 'number' 형식에 할당할 수 없습니다.
const log3: Person = { name: '로그', age: 20, hobby: '컴퓨터' }; // ❌ 개체 리터럴은 알려진 속성만 지정할 수 있으며 'Person' 형식에 'hobby'이(가) 없습니다.
```

<br/>

---
## 5.3 인터페이스를 이용한 함수 타입 정의

객체는 함수의 파라미터로도 사용되고 반환값으로도 사용될 수 있다.  

<br/>

### 5.3.1 함수 파라미터 타입 정의

```TS
interface Person {
    name: string;
    age: number;
}

function printAge(someone: Person) {
    console.log(someone.age);
}

const log: Person = { name: '로그', age: 20 };
printAge(log);
```

### 5.3.2 함수 반환 타입 정의

 - 파라미터로 Person 인터페이스 타입의 데이터를 받아 타입 추론이 된다.
 - 또한, 함수의 반환 타입으로 명시적으로 표시할 수 있다.
```TS
interface Person {
    name: string;
    age: number;
}

function getPerson(someone: Person): Person {
    return someone;
}
```

<br/>

---
## 5.4 인터페이스의 옵션 속성

인터페이스에서도 선택적 프로퍼티를 설정할 수 있다.
 - 선택적 프로퍼티를 이용하면 상황에 따라서 유연하게 인터페이스 속성의 사용 여부를 결정할 수 있다.
 - 변수명 앞에 '?' 키워드를 정의한다.

```TS
interface Person {
    name: string;
    age?: number;
}

function printName(someone: Person) {
    console.log(someone.name);
}
function printPersonInfo(someone: Person) {
    console.log(`이름: {someone.name}, 나이: {someone.age}`);
}

const log = { name: '로그' };
printName(name);
```

<br/>

---
## 5.5 인터페이스 상속

상속은 객체 간 관계를 형성하는 방법으로, 상위 클래스의 내용을 하위 클래스가 물려받아 사용하거나 확장하는 기법을 의미한다.

 - Javascript 상속 예제 코드
    - 클래스를 상속받을 때 extends 키워드를 사용한다.
    - Person 클래스를 정의하고, Developer 클래스에서 상속받아 클래스 내부를 구현
```JS
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    printAge() {
        console.log(this.age);
    }
}

class Developer extends Person {
    constructor(name, age, skill) {
        super(name, age);
        this.skill = skill;
    }

    printDeveloperInfo() {
        this.printAge();
        console.log(this.name);
        console.log(this.skill);
    }
}

var log = new Developer('로그', 20, 'Java');
log.printDeveloperInfo(); // 20, 로그, Java
```

<br/>

### 5.5.1 인터페이스의 상속이란?

클래스를 상속받을 때 extends라는 예약어를 사용한다.  
인터페이스를 상속받을 때에도 동일하게 extends 예약어를 사용한다.

 - Person 인터페이스를 선언하고 Developer 인터페이스에 extends로 상속한다.
```TS
interface Person {
    name: string;
    age: number;
}

interface Developer extends Person {
    skill: string;
}

var log: Developer = {
    name: '로그',
    age: 20,
    skill: 'Java'
};
```

 - Person 인터페이스에 정의된 name과 age 속성 타입이 Developer 인터페이스에 상속되어 아래와 같이 정의한 효과가 나타난다.
```TS
interface Developer {
    name: string;
    age: number;
    skill: string;
}
```

<br/>

### 5.5.2 인터페이스를 상속할 때 참고 사항

상위 인터페이스의 타입을 하위 인터페이스에서 상속받아 타입을 정의할 때 상위 인터페이스의 타입과 호환이 되어야 한다.  
즉, 상위 클래스에서 정의된 타입을 사용해야 한다는 의미이다.
또한, 상속을 여러 번 할 수 있다.

```TS
interface Hero {
    power: boolean;
}

interface Person extends Hero {
    name: string;
    age: number;
}

interface Developer extends Person {
    skill: string;
}

const ironman: Developer = {
    name: '아이언맨',
    age: 20,
    skill: '만들기',
    power: true
};
```

<br/>

---
## 5.6 인터페이스를 이용한 인덱싱 타입 정의

인덱싱이란 객체의 특정 속성을 접근하거나 배열의 인덱스로 특정 요소에 접근하는 동작을 의미한다.  

 - user['name'] 형태로 객체의 특정 속성에 접근하거나, companies[0] 형태로 배열의 특정 요소에 접근하는 것을 인덱싱이라고 한다.
```TS
const user = {
    name: '로그',
    age: 20
};
console.log(user['name']); // 로그

const companies = ['삼성', '네이버', '구글'];
console.log(companies[0]); // 삼성
```

<br/>

### 5.6.1 배열 인덱싱 타입 정의

배열을 인덱싱할 때 인터페이스로 인덱스와 요소의 타입을 정의할 수 있다.

 - 아래 예제는 배열의 인덱스 타입이 [index: number]가 되고, 인덱스로 접근한 요소의 타입이 string이 된다.
```TS
interface StringArray {
    [index: number]: string;
}

const companies: StringArray = ['삼성', '네이버', '구글'];

companies[0]; // 삼성
companies[1]; // 네이버
```

### 5.6.2 객체 인덱싱 타입 정의

객체 인덱싱의 타입도 인터페이스로 정의할 수 있다.

```TS
// 속성 이름이 문자열 타입이고, 속성 값이 숫자 타입인 모든 속성 이름/속성 값 쌍을 허용
interface SalaryMap {
    [level: string]: number;
}

const salary: SalaryMap = {
    junior: 100
};

const money = salary['jonior'];
```

### 5.6.3 인덱스 시그니처란?

정확히 속성 이름을 명시하지 않고 속성 이름의 타입과 속성 값의 타입을 정의하는 문법을 인덱스 시그니처라고 한다.  
인덱스 시그니처는 단순히 객체와 배열을 인덱싱할 때 활용될 뿐만 아니라 객체의 속성 타입을 유연하게 정의할 때에도 사용된다.

```TS
// 단순 객체 타입 정의
interface SalaryInfo {
    junior: string;
}

// ❌ 인터페이스 타입과 객체 타입이 맞지 않아 에러가 발생한다.
// 속성이 추가될 때마다 인터페이스에도 추가되어야 한다.
const salary: SalaryInfo = {
    junior: '100원',
    mid: '400원',
    senior: '700원'
};

// 인덱스 시그니처 정의
interface SalaryInfo {
    [level: string]: string;
}

// ✔ 속성 이름이 문자열이고 속성 값의 타입이 문자열이기만 하면 무수히 많은 속성을 추가해도 된다.
const salary: SalaryInfo = {
    junior: '100원',
    mid: '400원',
    senior: '700원',
    ceo: '0원',
    newbie: '50원'
};
```

### 5.6.4 인덱스 시그니처를 언제 쓸까?

객체의 속성 이름과 개수가 구체적으로 정의되어 있다면 인터페이스에서 속성 이름과 속성 값의 타입을 명시하는 것이 더 효과적이다.  
인덱스 시그니처가 적용되면, 코드를 작성할 때 구체적으로 어떤 속성이 제공될지 알 수 없어 코드 자동 완성이 되지 않는다.  
떄문에, 객체의 속성 이름과 속성 값이 정해져 있는 경우에는 속성 이름과 속성 값 타입을 명시해서 정의하고, 속성 이름은 모르지만 속성 이름의 타입과 값의 타입을 아는 경우에는 인덱스 시그너치를 활용한다.

```TS
interface Person {
    [property: string]: string
    id: string;
    name: string;
}

const log: Person = {
    id: '1',
    name: '로그',
    address: '서울'
};
```