# 16. 타입 모듈

## 16.1 모듈이란?

모듈은 프로그래밍 관점에서 특정 기능을 갖는 작은 단위의 코드를 의미한다.  
애플리케이션 규모가 커질수록 이러한 모듈이 중요해진다.  
모듈은 수많은 함수와 변수, 클래스 등 논리적인 단위로 구분하여 필요할 때 가져다 쓸 수 있는 개념을 의미한다.

<br/>

---
## 16.2 자바스크립트 모듈

자바스크립트는 태생적으로 모듈이라는 개념이 없던 프로그래밍 언어이다.  
때문에, 파일 단위로 변수나 함수가 구분되지 않아 문제점이 많았다.
 - 자바스크립트에서 코드를 파일별로 변수나 함수를 구분해서 정의하더라도 기본적으로 모두 전역 유효 범위를 갖는다.
 - 때문에, 이름이 서로 충돌할 수 있는 문제가 있다.

<br/>

### 16.2.1 자바스크립트 모듈화를 위한 시도

초창기 자바스크립트는 모듈을 지원하지 않았다.  
때문에, 불편함을 느낀 사용자들은 모듈화를 지원하려는 시도를 하여 Common.js와 Require.js를 개발한다.  
 - Common.js는 브라우저뿐만 아니라 브라우저 이외의 환경인 서버, 데스크톱에서도 자바스크립트를 활용하려고 고안된 스팩이자 그룹이다. 현재는 서버 런타임 환경인 Node.js에서 기본 모듈로 사용된다.
    - module.exports로 모듈을 내보낸다.
    - require()로 모듈을 불러온다.
```TS
// math.js
function sum(a, b) {
    return a + b;
}

module.exports = {
    sum
};

// app.js
var math = require('./math.js');

console.log(math.sum(1, 2)); // 3
```

 - Require.js는 AMD라는 비동기 모듈 정의 그룹에서 고안된 라이브러리 중 하나이다.
 - 비동기 모듈은 애플리케이션이 시작되었을 때 모든 모듈을 가져오는 것이 아니라 필요할 때 순차적으로 해당 모듈을 가져온다는 의미이다.
    - require() 문법으로 외부 라이브러리를 가져온다.
    - 외부 라이브러리가 정상적으로 로드되면 콜백 함수가 실행된다.
```HTML
<body>
    <!-- 라이브러리 파일 다운로드 후 다음과 같이 연결 -->
    <script src="requiore.js"></script>
    <script>
        require(["JS 파일 주소"], function() {
            console.log("모듈이 로드되었습니다.");
        });
    </script>
</body>
```

<br/>

---
## 16.3 자바스크립트 모듈화 문법

자바스크립트 생태계에서 언어 레벨에서 지원되지 않는 모듈화 개념으로 인해 불편함이 많았다.  
때문에, 2015년에 언어 레벨에서 import/export 키워드로 표준 문법을 제공하게 된다.  

<br/>

### 16.3.1 import와 export

2015년 자바스크립트를 의미하는 ES6(ECMAScript 2015)부터 import와 export 문법을 지원한다.
 - export로 모듈을 내보낸다.
 - import로 모듈을 불러온다.
```JS
// math.js
function sum(a, b) {
    return a + b;
}

export { sum }

// app.js
import { sum } from './math.js'
console.log(sum(10, 20));
```

### 16.3.2 export default 문법

export 문법에 default 구문을 사용할 수 있다.  
export default는 해당 파일에서 하나의 대상만을 내보내겠다는 의미이다.  

```TS
// math.js
function sum(a, b) {
    return a + b;
}
export default sum;

// app.js
import sum from './math.js';
console.log(sum(10, 20));

// default를 사용하지 않았을 때: import { sum } from './math.js';
// default를 사용했을 때: import sum from './math.js';
```

<br/>

### 16.3.3 import as 문법

import 구문에 as 키워드를 이용하면 가져온 변수나 함수의 이름을 해당 모듈 내에서 변경하여 사용할 수 있다.

```TS
// math.js
function sum(a, b) {
    return a + b;
}
export { sum };

// app.js
import { sum as add } from './math.js';
console.log(add(10, 20));
```

<br/>

### 16.3.4 import * 문법

특정 파일에서 내보낸 기능이 많아 import 구문으로 가져와야 할 것이 많다면 * 키워드를 사용하여 편리하게 가져올 수 있다.  
 - export 키워드로 지정한 모든 변수와 함수를 특정 이름으로 붙여 사용할 것으로 지정한다.
```JS
// math.js
function sum(a, b) {
    return a + b;
}

function sub(a, b) {
    return a - b;
}

function div(a, b) {
    return a / b;
}

export { sum, substract, divide };

// app.js
import * as myMath from './math.js'
console.log(myMath.sum(10, 20)); // 30
console.log(myMath.sub(30, 10)); // 20
console.log(myMath.div(4, 2));   // 2
```
 - 위에 예제에서 myMath를 네임스페이스라고 봐도 되고, 다음과 같이 객체라고 생각해도 된다.
```TS
var myMath = {
    sum: function(a, b) {
        return a + b;
    },
    sub: function(a, b) {
        return a - b;
    },
    div: function(a, b) {
        return a / b;
    }
}
```

<br/>

### 16.3.5 export 위치

export는 특정 파일에서 다른 파일이 가져다 쓸 기능을 내보낼 때 사용하는 키워드이다.  
변수나 함수, 클래스에 모두 사용할 수 있다.

 - 변수, 함수, 클래스 등 코드를 작성하고 파일의 마지막 줄에 export로 내보낼 대상 정의
```JS
const PI = 3.14;
const getHello = () => {
    return 'Hello';
};
class Person {
    ..
}

export { PI, getHello, Person }
```
 - 내보낼 대상 앞에 바로 export 정의
    - 마지막 줄에 export 구문을 추가할 필요가 없어 직관적인 부분이 있다.
    - 하지만, 내보낼 대상이 많아지면 export 키워드를 일일이 붙여야 하기 때문에 코드 반복이 많아진다.
    - 개인 취향에 따라 어느 방식을 선택하든 상관없지만, 일관성을 유지하는 것이 중요하다.
```JS
export const PI = 3.14;
export const getHello = () => {
    return 'Hello';
};
export class Person {
    ..
}
```

<br/>


---
## 16.4 타입스크립트 모듈

타입스크립트의 모듈은 자바스크립트 모듈화 개념과 문법 그대로 적용하면 된다.  
타입스크립트파일에 작성된 변수, 함수, 클래스 등 기능을 import, export 문법으로 내보내거나 가져올 수 있다.

```TS
// math.ts
function sum(a: number, b: number) {
    return a + b;
}
export { sum }

// person.ts
interface Person {
    name: string;
    age: number;
}
export { Person }

// app.ts
import { sum } from './math.ts';
import { Person } from './person.ts';

console.log(sum(10, 20)); // 30
var log: Person = {
    name: '로그',
    age: 20
};
```

<br/>

---
## 16.5 타입스크립트 모듈 유효 범위

타입스크립트 모듈을 다룰 떄는 변수나 함수의 유효 범위를 알아두어야 한다.  
자바스크립트가 변수를 선언할 떄 기본적으로 전역 변수로 선언되듯이 타입스크립트 역시 전역 변수로 선언된다.  
 - 모두 전역으로 선언되기 떄문에, 동일한 변수명이 존재하면 이미 정의되어 있다는 에러가 발생한다.
 - 또한, interface는 동일한 이름의 인터페이스가 존재할 경우 병합되기 때문에 주의해야 한다.
```TS
// util.ts
const a: number = 10; // ❌ Cannot redeclare block-scoped variable 'a'.ts(2451) app.ts(1, 7): 'a' was also declared here.

// app.ts
const a: string = 'Hello'; // ❌ Cannot redeclare block-scoped variable 'a'.ts(2451) util.ts(1, 7): 'a' was also declared here.
```

<br/>

---
## 16.6 타입스크립트 모듈화 문법

### 16.6.1 import type 문법

타입을 가져올 떄 자바스크립트 모듈과 동일하게 import 구문을 사용할 수 있지만, 타입 코드일 때는 type이라는 키워드를 추가로 사용할 수 있다.  
 - 타입을 다른 파일에서 import로 가져오는 경우 import type을 사용하여 타입 코드인지 아닌지 명시할 수 있다.
```TS
// hero.ts
interface Hulk {
    name: string;
    skill: string;
}
export { Hulk };

// app.ts
import type { Hulk } from './hero';

var banner: Hulk = {
    name: '배너',
    skill: '화내기',
}
```

<br/>

### 16.6.2 import inline type 문법

import inline type 문법은 변수, 함수 등 실제 값으로 쓰는 코드와 타입 코드를 같이 가져올 때 사용할 수 있다.  
여러 개를 가져올 때 어떤 코드가 타입인지 구분할 수 있는 장점이 있다.  
 - 특정 파일에서 인터페이스, 함수, 변수를 export를 내보낼 때 불러오는 곳에서 import로 가져온다.
 - 이때, import 내부에 type 키워드를 사용하여 가져오는 코드가 타입인지 아닌지 명시할 수 있다.
```TS
// hero.ts
interface Hulk {
    name: string;
    skill: string;
}

function smashing() {
    return '';
};

var doctor = {
    name: '스트레인지'
}

export { Hulk, smashing, doctor };

// app.ts
import { type Hulk, doctor, smashing } from './hero';

var banner: Hulk = {
    name: '배너',
    skill: '화내기',
}
```

<br/>

### 16.6.3 import와 import type 중 어떤 문법을 써야 할까?

가장 중요한 것은 코딩 컨벤션을 따르는 것이다.  
혼자서 진행하는 프로젝트라면 스스로 규칙을 정하고 일관적으로 작성하면 된다.  
 - 자동 완성으로 작성된 import 구문에는 type 키워드가 별도로 붙지 않는다.
 - 때문에, 실무에서는 많은 코드가 import 구문 안에서 변수/함수와 타입을 구분하지 않는 경우가 많다.
 - 자동 완성이 주는 편리함을 따라간다면 type을 붙이지 않고, 코드 역할을 좀 더 명확하게 하겠다면 type을 붙이면 된다.

<br/>

---
## 16.7 모듈화 전략: Barrel

여러 개의 파일에서 모듈을 정의하여 가져올 때 배럴(Barrel)이라는 전략을 사용할 수 있다.  
배럴이란 여러 개의 파일에서 가져온 모듈을 마치 하나의 통처럼 관리하는 방식이다.
 - 기본적으로 모듈을 불러올 때 해당 파일명으로 찾고, 파일이 없는 경우 해당 폴더안에 index.js 파일을 불러들인다.
    - 즉, 성격이 비슷한 모듈들을 하나의 폴더안에서 관리한다.
    - 모든 모듈을 불러들일 수 있는 index.js 파일을 생성한다.
    - 사용하는 곳에서는 해당 폴더를 불러오면 index.js 파일을 통해 모든 모듈이 불러진다.

<br/>

### 16.7.1 Barrel 모듈화 전략 예제
 - hero 폴더에 성격이 비슷한 3개의 모듈이 존재한다.
    - 이러한 경우 사용하는 곳에서 import를 3번을 하여 각각의 모듈을 가져올 수 있다.
    - 하지만, 이러한 방법은 비슷한 성격의 코드임에도 import 구문 숫자가 많아져 가독성이 떨어질 수 있다.
    - 때문에, hero 폴더에 3개 모듈을 한 곳에 모아주는 중간 파일을 생성하여 관리할 수 있다.
```TS
// ./hero/hulk.ts
interface Banner {
    name: string;
}
export { Banner }

// ./hero/ironman.ts
interface Tony {
    name: string;
}
export { Tony }

// ./hero/captain.ts
interface Steve {
    name: string;
}
export { Steve }

// ./hero/index.ts
export { Banner } from './hulk';
export { Tony } from './ironman';
export { Steve } from './captain';

// app.ts
// import { Banner } from './hulk';
// import { Tony } from './ironman';
// import { Steve } from './captain';
import { Banner, Tony, Steve } from './hero';

var banner: Banner = { name: '배너' };
var tony: Tony = { name: '토니' };
var steve: Steve = { name: '스티브' };
```