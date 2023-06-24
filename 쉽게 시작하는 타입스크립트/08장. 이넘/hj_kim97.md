# 8. 이넘

## 8.1 이넘이란?

이넘은 특정 값의 집합을 의미하는 데이터 타입이다.  
상수는 단순히 고정된 값을 저장하는 것뿐만 아니라 이 값이 어떤 의미를 갖는 지 알려줌으로써 가독성을 높이는 장점이 있다.  
여러 개의 상수를 하나의 단위로 묶으면 이넘이 되는데, 이넘을 상수 집합이라고도 표현한다.

```TS
// 상수
const RICE = 10000;
const COKE = 20000;

// 이넘
enum ShoesBrand {
    Nike,       // 0
    Adidas,     // 1
    NewBalance  // 2
}

// 객체의 속성에 접근하듯이 이넘의 이름을 쓰고 . 접근자를 이용하여 속성 이름을 붙인다.
const myShoes = ShoesBrand.Nike; // 0
const yourShoes = ShoesBrand.NewBalance; // 2
```

<br/>

---
## 8.2 숫자형 이넘

이넘에 선언된 속성은 기본적으로 숫자 값을 가진다.  
만약, 이넘 속성의 초기값을 변경하고 싶다면 이넘 안에 상수에 값을 정의하면 된다.  

```TS
// 이넘
enum ShoesBrand {
    Nike,       // 0
    Adidas,     // 1
    NewBalance  // 2
}

console.log(ShoesBrand.Nike); //0
console.log(ShoesBrand[0]); // 'Nike'

// 이넘 속성의 초기값 정의
enum Direction {
    Up = 10,    // 10
    Down,       // 11
    Left,       // 12
    Right,      // 13
}

console.log(Direction.Up); // 10
console.log(Direction[10]); // 'Up'
```

<br/>

---
## 8.3 문자형 이넘

문자형 이넘이란 이넘의 속성 값에 문자열을 연결한 이넘을 의미한다.  
숫자형 이넘과 다르게 모든 속성 값을 다 문자열로 지정해주어야 한다.  
선언된 속성 순서대로 값이 증가하는 규칙도 없다.
 - 실무에서는 이넘 값을 숫자로 관리하기보다 문자열로 관리하는 사례가 더 많다.
 - 속성 이름과 값을 동일한 문자열로 관리하는 것도 일반적인 코딩 규칙으로 사용될 수 있다.
 - 이넘의 속성을 모두 대문자로 적거나 언더스코어(_)를 사용하는 경우도 많다.

```TS
// 문자형 이넘
enum Direction {
    Up = 'Up'
    Down = 'Down',
    Left = 'Left',
    Right = 'Right'
}

console.log(Direction.Up); // 'Up'

// 언더스코어 사용
enum ArrowKey {
    KEY_UP = 'KEY_UP',
    KEY_DOWN = 'KEY_DOWN'
}
```

<br/>

---
## 8.4 알아두면 좋은 기넘의 특징

### 8.4.1 혼합 이넘

이넘의 속성들에 대해서 숫자와 문자열을 섞어서 선언할 수 있다.  
혼합으로 사용해도 코드상으로는 문제가 없지만, 이넘 값은 일괄되게 숫자나 문자열 둘 중 하나의 데이터 타입으로 관리하는 것이 좋다.  

```TS
enum Answer {
    YES = 'YES',
    NO = 1
}
```

<br/>

### 8.4.2 다양한 이넘 속성 값 정의 방식

이넘의 속성 값은 고정 값뿐만 아니라 다양한 형태로 값을 할당할 수 있다.

 - User와 Admin 속성은 이넘의 기본 규칙에 따라 값이 0과 1이 된다.
 - SuperAdmin 속성은 User와 Admin의 값을 더한 1이 된다.
 - God 속성은 "abc" 문자열의 길이인 3이 된다.
```TS
enum Authorization {
    User,                       // 0
    Admin,                      // 1
    SuperAdmin = User + Admin,  // 1
    God = "abc".length          // 3
}
```

<br/>

### 8.4.3 const 이넘

const 이넘이란 이넘을 선언할 때 앞에 const를 붙인 이넘을 의미한다.  
const는 변수를 선언할 떄 사용하는 예약어로, 이넘 타입을 정의할 때에도 사용할 수 있다.  
const 이넘을 사용하면, 컴파일시 이넘이 사용되는 곳에서 객체를 생성하지 않고 속성 값을 바로 연결해준다.  
때문에, 컴파일 코드 양을 줄여준다.  
 - const 이넘은 항상 속성에 고정 값을 넣어주어야 한다.

```TS
enum LogLevel {
    Debug = 'Debug',
    Info = 'Info',
    Error = 'Error'
}

const applicationLogLevel = LogLevel.Error;
```