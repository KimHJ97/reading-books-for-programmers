# 13. 타입 단언

## 13.1 타입 단언이란?

타입 단언은 타입스크립트의 타입 추론에 기대지 않고 개발자가 직접 타입을 명시하여 해당 타입으로 강제하는 것을 의미한다.  
 - as 키워드를 붙이면 타입스크립트가 컴파일할 때 해당 코드의 타입 검사는 수행하지 않는다.
 - 타입 단언을 사용하면 타입스크립트 컴파일러가 알기 어려운 타입에 대해 힌트를 제공할 수 있다.

```TS
var name = '로그' as string;

interface Person {
    name: string;
    age: number;
}

var log = {} as Person; // 변수를 빈 객체로 선언했지만, 타입 단언으로 Person 타입임을 보장한다.
log.name = '로그';
log.age = 20;
```

<br/>

---
## 13.2 타입 단언 문법

타입 단언 키워드인 as를 이용할 수 있는 대상과, 타입 단언을 중첩해서 쓰는 방법, 단언을 사용할 떄 유의할 점을 알아보자.

<br/>

### 13.2.1 타입 단언 대상

타입 단언은 숫자, 문자열, 객체 등 원시 값뿐만 아니라 변수나 함수의 호출 결과에도 사용할 수 있다.

```TS
function getId(id) {
    return id;
}

var id = getId('hj_kim97') as number;
```

<br/>

### 13.2.2 타입 단언 중첩

타입 단언은 여러 번 중첩해서 사용할 수도 있다.

```TS
var num1 = 10 as any; // any 타입 추론
var num2 = (10 as any) as number; // any -> number 타입 추론
```

<br/>

### 13.2.3 타입 단언을 사용할 떄 주의할 점

 - as 키워드는 구문 오른쪽에서만 사용한다.

타입 단언은 변수 이름에 사용할 수 없다.

```TS
var num as number = 10; // ❌ 컴파일 에러
var num = 10 as number; // ✔ 정상 동작
```

 - 호환되지 않는 데이터 타입으로는 단언할 수 없다.

타입 단언 대상끼리 슈퍼-서브 타입 관계를 갖고 있어야 한다. (교차점이 있어야 한다.)

```TS
let num1 = 10 as never;   // ✅ never 타입은 모든 타입의 서브 타입으로 A가 B의 슈퍼타입이다.
let num2 = 10 as unknown; // ✅ unknown 타입은 모든 타입의 슈퍼 타입이므로 A가 B의 서브 타입이다.

let num3 = 10 as string;  // ❌ number 타입과 string 타입은 서로 슈퍼-서브 타입 관계를 갖지 않는다.
```

<br/>

---
## 13.3 null 아님 보장 연산자: !

null 아님 보장 연산자는 null 타입을 체크할 때 유용하게 쓰는 연산자이다.  
Non Null 단언이라고도 불린다.  
 - 값 뒤에 느낌표(!)를 붙여주면 이 값이 undefined나 null이 아닐 것으로 단언할 수 있다.
 - 다만, 타입 관점에서 null이 아니라고 보장하는 것이지 애플리케이션을 실행할 때 실제로 null 값이 들어오면 실행 에러가 발생할 수 있으므로 주의가 필요하다.
 - 즉, as나 !를 사용한 타입 단언이 편리하긴 하지만, 실행 시점의 에러를 막아 주지 않기 떄문에 가급적 타입 단언보다는 타입 추론이 권장된다.

```TS
type Post = {
  title: string;
  author?: string;
};

let post: Post = {
  title: "게시글1",
};

const len: number = post.author!.length;
```