# 6. 연산자를 사용한 타입 정의

자바스크립트의 OR 연산자인 ||와 AND 연산자인 &&의 기호를 따서 타입을 정의할 수 있다.

<br/>

## 6-1. 유니언 타입

유니언 타입은 여러 개의 타입 중 한 개만 쓰고 싶을 때 사용하는 문법이다.

```TS
// 문자열과 숫자를 모두 받을 수 있는 유니언 타입 설정
function printText(text: string | number) {
    console.log(text);
}

printText('hello');
printText(100);
```

<br/>

---
## 6-2. 유니언 타입의 장점

유니언 타입을 이용해서 하나의 함수에 여러 타입의 매개변수를 받을 수 있게 되었다.  
만약, 유니언 타입을 이용하지 않았더라면 동일한 동작을 하는 함수더라도 타입이 다르다는 이유로 함수를 하나 더 작성해서 관리해야 하는 불편함이 있다.  
이럴 때 유니언 타입을 사용해서 같은 동작을 하는 함수의 코드 중복을 줄일 수 있다.

 - any 타입을 이용하여 여러 개의 타입을 받을 수 있지만, 이는 타입이 없는 것과 마찬가지로 타입스크립트의 이점을 살리지 못하게 된다.
```TS
function printText(text: any) {
    console.log(text);
}

printText('hello');
printText(100);
```

<br/>

---
## 6-3. 유니언 타입을 사용할 때 주의할 점

유니언 타입을 사용할 때 여러 개의 타입이 올 수 있기 떄문에 발생할 수 있는 문제가 있다.  

 - 아래 예제 코드는 name과 age 속성을 가진 Person 인터페이스와 name과 skill 속성을 가진 Developer 인터페이스를 정의한다.
    - 공통 속성은 name이고, age와 skill은 각 인터페이스 고유의 값이다.
 - 유니언 타입을 이용하여 Person과 Developer을 매개변수로 받아 출력하는 introduce 함수를 정의한다.
    - 해당 파라미터에서 someone.age나 someone.skill을 출력하게 되면, 타입에 따라서 존재할 수도 있고, 존재하지 않을 수도 있게 된다.
    - 때문에, 컴파일 전에 에러 문구 확인을 할 수 있다. 실제로 실행하면 undefined 값이 반환되고, 함수인 경우라면 에러가 발생하게 된다.
    - 이처럼 어떤 값이 들어올지 알 수 없을 때에 특정 타입의 고유한 함수나 값을 사용하고 싶은 경우에는 in 연산자를 이용해서 타입에 안전성을 추가해준다.
 - in 연산자는 객체에 특정 속성이 있는지 확인하는 자바스크립트 연산자이다.
    - 객체에 해당 속성이 있으면 true를 반환하고 그렇지 않으면 false를 반환한다.
```TS
interface Person {
    name: string;
    age: number;
}

interface Developer {
    name: string;
    skill: string;
}

function introduce(someone: Person | Developer) {
    console.log(someone);
    console.log(someone.age); // ❌ 타입이 Person인지 Developer인지 모름.
}

function introduce2(someone: Person | Developer) {
    if ('age' in someone) {
        console.log(someone.age); // ✔ someone 파라미터가 Person 타입으로 간주된다.
        return;
    }
    if ('skill' in someone) {
        console.log(someone.skill); // ✔ someone 파라미터가 Developer 타입으로 간주된다.
        return;
    }
}
```

 - typeof 연산자는 해당 데이터가 어떤 데이터 타입을 갖고 있는지 문자열로 반환해준다.
    - 문자면 string, 숫자면 number, 함수면 function 등
```TS
function printText(text: string | number) {
    if (typeof text === 'string') {
        console.log(text.toUpperCase()); // ✔ text 파라미터가 string 타입으로 추론된다. string 내부 함수 사용 가능
    }
    if (typeof text === 'number') {
        console.log(text.toLocaleString()); // ✔ text 파라미터가 number 타입으로 추론된다. number 내부 함수 사용 가능
    }
}
```

<br/>

---
## 6-4. 인터섹션 타입

인터렉션 타입은 타입 2개를 하나로 합쳐서 사용할 수 있는 타입이다.  
보통 인터페이스 2개를 합치거나 타입 정의 여러 개를 하나로 합칠 때 사용한다.  

 - 인터섹션 타입은 결합된 타입의 모든 속성을 만족하는 객체를 인자로 넘겨야 한다.
```TS
// 펜 ()
interface Pen {
    leadSize: number
}

// 색상
interface Color {
    color: string;
}

function write(colorPen: Pen & Color) {
    console.log('색상: ', colorPen.color);
    console.log('심의 사이즈: ', colorPen.leadSize);
    console.log('색연필로 글쓰기 진행');
}

write({ leadSize: 0.7, color: '검정' }); // ✔
write({ leadSize: 0.7 }); // ❌ 속성이 하나라도 누락시 에러 발생
```