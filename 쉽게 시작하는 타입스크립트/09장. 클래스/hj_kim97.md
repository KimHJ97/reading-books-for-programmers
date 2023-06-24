# 9. 클래스

## 9.1 클래스란?

클래스란 여러 가지 유사한 객체를 쉽게 생성하는 자바스크립트 최신 문법(ES6+) 이다.
 - ES6는 ECMAScript 2015를 의미하고, ES6+는 ECMAScript 2015 ~ 현재를 의미한다.
 - 생성자 함수를 정의하고, new 키워드로 호출하여 새로운 객체를 생성할 수 있었다.
    - 생성자 함수와 클래스는 코드는 다르지만 역할이 동일하다.
    - 즉, 생성자 함수라는 일반적인 관례를 문법 레벨로 끌어올린 것이 클래스이다.
```JS
// ES6 이전
function Person(name, age) {
    this.name = name;
    this.age = age;
}

var log = new Person('로그', 20);
console.log(log.age); // 20

// ES6 이후
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }
}

var log = new Person('로그', 20);
console.log(log.age); // 20
```

<br/>

---
## 9.2 클래스 기본 문법


```JS
// ES6 이전
function Person(name, age) {
    this.name = name;
    this.age = age;
}

Person.prototype.sayHello = function() {
    console.log('Hello!');
}

var log = new Person('로그', 20);
console.log(log.age); // 20
log.sayHello(); // Hello!

// ES6 이후
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    sayHello() {
        console.log('Hello!');
    }
}

var log = new Person('로그', 20);
console.log(log.age); // 20
log.sayHello(); // Hello!
```

<br/>

---
## 9.3 클래스의 상속

클래스의 상속이란 부모 클래스의 속성과 메서드 등을 자식 클래스에서도 사용할 수 있게 물려준다는 의미이다.  
클래스 상속은 extends 키워드를 이용한다.

```JS
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    sayHello() {
        console.log('Hello!');
    }
}

class Developer extends Person {
    constructor(name, age, skill) {
        super(name, age);
        this.skill = skill;
    }

    coding() {
        console.log(`${this.skill}를 이용하여 코딩중입니다.`);
    }
}

var log = new Developer('로그', 20, 'Typescript');
log.coding(); // Typescript를 이용하여 코딩중입니다.
log.sayHello(); // Hello!
```

<br/>

---
## 9.4 타입스크립트의 클래스

타입스크립트의 클래스는 자바스크립트 클래스에 타입을 추가하면 된다.  
주의할 점으로는 타입스크립트로 클래스를 작성할 때는 생성자 메서드에서 사용될 클래스 속성들은 미리 정의해 주어야 한다.

```TS
// 자바스크립트 클래스
class Chatgpt {
    constructor(name) {
        this.name = name;
    }

    sum(a, b) {
        return a + b;
    }
}

// 타입스크립트 클래스
class Chatgpt {
    name: string;

    constructor(name: string) {
        this.name = name;
    }

    sum(a: number, b: number): number {
        return a + b;
    }
}
```

<br/>

---
## 9.5 클래스 접근 제어자

접근 제어자는 클래스 속성의 노출 범위를 말한다.  
기능을 구현할 때 여러 개의 객체를 다루다 보면 의도치 않게 특정 객체 값이 바뀌어 에러로 이어지는 경우가 있다.  
이러한 경우 클래스 속성의 접근 제어자를 이용하면 의도치 않은 에러가 발생할 확률을 낮출 수 있다.  

### 9.5.1 클래스 접근 제어자: public, private, protected

클래스의 접근 제어자는 public, private, protected 3 가지가 존재한다.  

 - public
    - public 접근 제어자는 클래스 안에 선언된 속성과 메서드를 어디서든 접근할 수 있게 한다.
    - 클래스 속성과 메서드에 별도로 속성 접근 제어자를 선언하지 않으면 기본값은 public이 된다.
```TS
class Chatgpt {
    name: string;

    constructor(name: string) {
        this.name = name;
    }

    sum(a: number, b: number): number {
        return a + b;
    }
}

// 클래스의 속성과 메서드를 클래스 코드 밖에서 모두 접근 가능
var gpt = new Chatgpt('log');
console.log(gpt.name); // log
gpt.sum(1, 2); //3
```

 - private
    - private 접근 제어자는 클래스 코드 외부에서 클래스의 속성과 메서드를 접근할 수 없다.
    - public과 반대되는 개념으로 클래스 안 로직을 외부 세상에서 단절시켜 보호할 때 주로 사용한다.
```TS
class Account {
    private id: string;
    private password: string;

    constructor(name: string, password: string) {
        this.id = id;
        this.password = password;
    }

    public changePassword(password) {
        this.password = password;
    }
}

var logAccount = ('log', '1234');
log.password = '1234@!'; // ❌ 해당 속성의 접근제어자가 private으로 접근이 불가능
log.changePassword('1234@!'); // ✔ changePassword로 클래스 내부의 password 속성 값 변경
```

 - protected
    - protected 접근 제어자는 private과 비슷하면서도 다르다.
    - protected로 선언된 속성이나 메서드는 클래스 코드 외부에서 사용할 수 없다.
    - 다만, 상속받은 클래스에서는 사용할 수 있다.
```TS
class Person {
    private name: string;
    private age: number;

    constructor(name: string, age: number) {
        this.name = name;
        this.age = age;
    }

    protected printAge(): void {
        console.log(this.age);
    }
}

class Developer extends Person {
    private skill: string;

    constructor(name: string, age: number, skill: string) {
        super(name, age);
        this.skill = skill;
        this.printAge();
    }

    public coding(): void {
        console.log(`${this.skill}을 이용하여 코딩중입니다.`);
    }
}
```