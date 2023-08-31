# 17. 유틸리티 타입

## 17.1 유틸리티 타입이란?

유틸리티 타입은 이미 정의되어 있는 타입 구조를 변경하여 재사용하고 싶을 때 사용하는 타입이다.  
타입스크립트에서 미리 정의해 놓은 내장 타입으로 타입스크립트를 설치한 후 타입스크립트 설정 파일의 lib 속성만 변경해 주면 바로 사용할 수 있다.  
 - 타입스크립트 설정 파일의 compilerOptions 속성에 lib 속성을 추가하면 된다.
    - lib 속성은 타입스크립트에서 미리 정의해 놓은 타입 선언 파일을 사용할 때 쓰는 옵션이다.
    - 자바스크립트 내장 API나 브라우저 DOM API 등을 스팩에 맞게 미리 정의해 두어 사용자가 가져가 쓸 수 있다.
```TS
{
    "compilerOptions": {
        "lib": ["ESNext"]
    }
}
```

<br/>

---
## 17.2 Pick 유틸리티 타입

Pick 유틸리티 타입은 특정 타입의 속성을 뽑아서 새로운 타입을 만들어 낼 떄 사용한다.  
 - Pick 타입으로 이미 존재하는 타입의 특정 속성만 추출해서 새로운 타입으로 정의할 수 있다.
```TS
// Pick 타입 문법
Pick<대상타입, '속성명'>
Pcik<대상타입, '속성명1' | '속성명2'>
```
 - Pick 타입 예시
```TS
// Pick 타입 예시
interface Profile {
    id: string;
    address: string;
}

type ProfileId = Pick<Profile, 'id'>;

var logProfile: ProfileId = {
    id: 'hj_kim97'
}

// Pick 타입 여러 개 추출 예시
interface HeroProfile {
    name: string;
    age: number;
    ability: string;
}

type PersonProfile = Pick<HeroProfile, 'name' | 'age'>;

var log: PersonProfile = {
    name: '로그',
    age: 20
}
```

<br/>

---
## 17.3 Omit 유틸리티 타입

Omit 타입은 특정 타입에서 속성 몇 개를 제외한 나머지 속성으로 새로운 타입을 생성할 때 사용하는 유틸리티 타입이다.  
Pick 타입은 특정 속성 몇 개를 뽑아서 타입을 생성하는 반면, Omit 타입은 특정 타입에서 속성 몇 개를 제외하고 나머지 타입으로 새로운 타입을 생성한다.  

```TS
// Omit 타입 문법
Omit<대상타입, '속성명'>
Omit<대상타입, '속성명1' | '속성명2'>
```
 - Omit 타입 예시
```TS
interface HeroProfile {
    name: string;
    age: number;
    ability: string;
}

type PersonProfile = Pick<HeroProfile, 'ability'>; // HeroProfile에서 ability를 제외한 타입으로 새로 생성한다.

var log: PersonProfile = {
    name: '로그',
    age: 20
}
```

<br/>

---
## 17.4 Partial 유틸리티 타입

Partial 타입은 특정 타입의 모든 속성을 모두 옵션 속성으로 변환한 타입을 생성해준다.  
즉, 특정 타입의 모든 속성을 선택적 속성으로 변경해준다.  
 - Pick 타입, Omit 타입과 다르게 대상 타입만 넘기면 된다.
```TS
// Partial 타입 문법
Partial<대상타입>
```
 - Partial 타입 예시
    - Partial 타입은 특정 타입의 속성을 모두 선택적으로 사용할 수 있으므로 보통 데이터 수정 API를 다룰 때 사용된다.
```TS
interface Todo {
    id: string;
    title: string;
    checked: boolean;
}

function updateTodo(todo: Partial<Todo>) {
    // ..
}

updateTodo({ id: '1' });
updateTodo({ id: '1', title: 'Partial 학습' });
updateTodo({ id: '1', title: 'Partial 학습', checked: true });
```

<br/>

---
## 17.5 Exclude 유틸리티 타입

Exclude 타입은 유니언 타입을 구성하는 특정 타입을 제외할 때 사용한다.  
Pick, Omit, Partial 타입은 모두 객체 타입의 형태를 변형하여 새로운 객체 타입을 만드는 반면 Exclude 타입은 유니언 타입을 변형한다.  
 - 첫 번째 제네릭 타입에 변형할 유니언 타입을 넣고, 두 번째 제네릭 타입으로 제외할 타입 이름을 문자열 타입으로 적거나 문자열 유니언 타입으로 넣어준다.
```TS
// Exclude 타입 문법
Exclude<대상유니언타입, '제거할 타입 이름'>
Exclude<대상유니언타입, '제거할 타입 이름1' | '제거할 타입 이름2'>
```
 - Exclude 타입 예시
```TS
type Languages = 'C' | 'Java' | 'Typescript' | 'React';
type TrueLanguages = Exclude<Languages, 'React'>; // "C" | "Java" | "Typescript"
```

<br/>

---
## 17.6 Record 유틸리티 타입

Record 타입은 타입 1개를 속성의 키로 받고 다른 타입 1개를 속성 값으로 받아 객체 타입으로 변환해준다.  
 - 첫 번쨰 제네릭 타입에는 객체 속성의 키로 사용할 타입을 넘기고, 두 번쨰 타입에는 객체 속성의 값으로 사용할 타입을 넘긴다.
    - 첫 번째 제네릭 타입에는 string, number, string 유니언, number 유니언 등이 들어 갈 수 있다.
    - 두 번재 제네릭 타입에는 아무 타입이나 들어갈 수 있다.
```TS
// Record 타입 문법
Record<객체속성의키로사용할타입, 객체속성의값으로사용할타입>
```
 - Record 타입 예시
```TS
interface HeroProfile {
    name: string;
    age: number;
    ability: string;
}
type HeroNames = 'thor' | 'hulk' | 'capt';

// Record 적용
type Heroes = Record<HeroNames, HeroProfile>;
```
 - 변환된 Heroes 타입
```TS
// Heroes 타입
type Heroes = {
    thor: HeroProfile;
    hulk: HeroProfile;
    capt: HeroProfile;
}

var avengers: Heroes = {
    thor: {
        name: '토르',
        age: 20,
        ability: '번개'
    },
    hulk: {
        name: '배너',
        age: 21,
        ability: '방사능 신체'
    }
    capt: {
        name: 'Steve',
        age: 22,
        ability: '각성된 신체'
    }
}
```

<br/>

---
## 17.7 그 외의 유틸리티 타입

타입스크립트는 기본적으로 다양한 내장 유틸리티 타입을 제공한다.  
Pick, Omit, Partial, Exclude, Record 이외에도 더 많은 유틸리티를 확인하고 싶으면 타입스크립트 공식 문서를 참고할 수 있다.  
 - [타입스크립트 공식 문서](https://www.typescriptlang.org/docs/handbook/utility-types.html)
