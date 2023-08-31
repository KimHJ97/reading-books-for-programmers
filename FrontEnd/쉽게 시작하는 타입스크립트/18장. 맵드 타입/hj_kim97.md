# 18. 맵드 타입

맵드 타입은 이미 정의된 타입을 가지고 새로운 타입을 생성할 때 사용하는 문법이다.  
유틸리티 타입은 모두 내부적으로 맵드 타입을 이용해서 구현되었다.  
맵드 타입을 이해하면 타입스크립트에서 이미 정의해 놓은 유틸리티 타입을 잘 사용할 수 있을 뿐만 아니라, 커스텀한 유틸리티 타입을 구현해서 사용할 수도 있다.

<br/>

---
## 18.1 맵드 타입 예시: in

 - in은 타입을 하나씩 순회한다.
```TS
type HeroNames = 'capt' | 'hulk' | 'thor';
type HeroAttendance = {
    [Name int HeroNames]: boolean;
}

// 맵드 타입으로 생성한 HeroAttendance 타입 정보
type HeroAttendance = {
    capt: boolean;
    hulk: boolean;
    thor: boolean;
}
```

<br/>

---
## 18.2 맵드 타입 예시: keyof

 - keyof는 특정 타입의 키 값만 모아 문자열 유니언 타입을 변환해주는 키워드이다.
```TS
interface Hero {
    name: string;
    skill: string;
}

// keyof Hero -> 'name' | 'skill'
// in keyof Hero -> in 'name' | 'skill' -> name과 skill 순회
type HeroPropCheck = {
    [H in keyof Hero]: boolean;
}

// 맵드 타입으로 생성한 HeroPropCheck 타입 정보
type HeroPropCheck = {
    name: boolean;
    skill: boolean
}
```

<br/>

---
## 18.3 맵드 타입을 사용할 떄 주의할 점

맵드 타입을 사용할 떄 인덱스 시그니처 문법 안에서 사용하는 in 앞의 타입 이름은 개발자가 마음대로 지정할 수 있다.

```TS
type HeroNames = 'capt' | 'hulk' | 'thor';

// #1
type HeroAttendance = {
    [Name in HeroNames]: boolean;
}

// #2
type HeroAttendance = {
    [HeroName in HeroNames]: boolean;
}
```

<br/>

두 번째로는 맵드 타입의 대상이 되는 타입 유형이다.  
문자열 유니언 타입, 인터페이스, 타입 별칭 등을 활용할 수 있다.

```TS
// 인터페이스 타입으로 맵드 타입을 생성
interface Hero {
    name: string;
    skill: string;
}

type HeroPropCheck = {
    [H in keyof Hero]: boolean;
}

// 타입 별칭으로 맵드 타입 생성
type Hero = {
    name: string;
    skill: string;
};

type HeroPropCheck = {
    [H in keyof Hero]: boolean;
}

// string 타입으로 맵드 타입 생성
type UserName = string;
type AddressBook = {
    [U in UserName]: number;
}
type AddressBook = { // 속성에 어떤 문자열이든 들어갈 수 있고 속성 값만 number 타입이 되면 된다.
    [x: string]: number
}
```

<br/>

---
## 18.4 매핑 수정자

매핑 수정자는 맵드 타입으로 타입을 변환할 때 속성 성질을 변환할 수 있도록 도와주는 문법이다.  
예를 들어 필수 속성 값을 선택적 속성 값으로 변환하거나 읽기 전용 속성을 내용을 변경할 수 있는 일반 속성으로 변환해준다.  
 - 매핑 수정자는 '+', '-', '?', 'readonly' 등이 있다.

<br/>

 - '?' 키워드 사용하기
    - '?' 매핑 수정자를 사용하면 선택적 속성으로 변경할 수 있다.
```TS
type Hero = {
    name: string;
    skill: string;
};

type HeroOptional = {
    [H in keyof Hero]?: string;
}

// 맵드 타입으로 변환된 HeroOptional
type HeroOptional = {
    name?: string;
    skill?: string;
}
```
 - '-' 키워드 사용하기
    - '-' 매핑 수정자를 사용하면 선택적 속성(?)이나 readonly 등 일반 속성 이외에 추가된 성질을 모두 제거할 수 있다.
```TS
type HeroOptional = {
    name?: string;
    skill?: string;
};

type HeroRequired<T> = {
    [Property in keyof T]-?: T[Property];
}

var capt: HeroRequired<HeroOptional> = {
    name: '캡틴',
    skill: '방패 던지기'
};
```

<br/>

---
## 18.5 맵드 타입으로 직접 유틸리티 타입 만들기

타입스크립트의 내장 유틸리티 타입은 모두 맵드 타입을 이용해서 구현되었다.  
즉, 맵드 타입을 이용하여 타입스크립트의 기본 내장 유틸리티 타입을 직접 구현할 수도 있다.  
객체 타입 속성을 모두 선택적 속성으로 바꾸어주는 Partial 타입을 직접 구현해보자.  

<br/>

 - 선택적 프로퍼티 맵드 타입
```TS
interface Todo {
    id: string;
    title: string;
}

type MyPartial = {
    [Property in keyof Todo]?: Todo[Property];
}

// 맵드 타입으로 변환된 MyPartial
type MyPartial = {
    id?: string;
    title?: string;
}
```
 - 제네릭을 이용하여 모든 타입에 사용 가능하도록 하기
    - 제네릭으로 넘겨받은 타입의 속성을 모두 옵션(선택적) 속성으로 변환해준다.
```TS
interface Todo {
    id: string;
    title: string;
}

interface Person {
    name: string;
    age: string;
}

// 제네릭으로 받은 Type과 맵드 타입에 Property의 이름은 T, P 같이 변경해도 된다.
type MyPartial<Type> = {
    [Property in keyof Type]?: Type[Property];
};

type TodoPartial = MyPartial<Todo>;
type PersonPartial = MyPartial<Person>;
```