# 03. 나의 첫 리액트 프로젝트

## 3.1 타입스크립트

자바스크립트는 동적 프로그래밍 언어로 런타임 시 변수의 타입이 결정된다.  
이렇게 런타임 중 변수의 타입이 결정되면서 발생하는 버그와 에러는 소스 코드를 실해아지 않으면 알 수가 없다.  

<br/>

이러한 문제를 해결하고자 리액트에서는 플로(Flow)라는 정적 타입 분석기 사용을 권장한다.  
플로는 페이스북에서 만든 정적 타입 분석기로, 리액트, 리액트 네이티브에서 변수에 타입을 미리 지정하여 변수의 타입으로 발생하는 문제를 해결할 수 있도록 도와주는 라이브러리이다.  

<br/>

하지만, 대부분의 많은 프로젝트에서는 플로 대신에 타입스크립트를 사용한다.  
플로는 리액트 전용 정적 타입 분석기로 개발된 반면에 타입스크립트는 자바스크립트 전반에 걸쳐 사용할 수 있도록 개발되었기 때문이다.  
따라서, 타입스크립트가 플로보다 좀 더 범용적으로 사용할 수 있어 이미 많은 자바스크립트 라이브러리에서 타입스크립트의 타입 정의 파일을 제공한다.  

<br/>

### 3.1.1 create-react-app과 타입스크립트

create-react-app으로 생성한 리액트 프로젝트에 타입스크립트를 적용하기 위해서는 타입스크립트 라이브러리와 리액트의 타입이 정의된 타입 정의 파일을 설치해야 한다.

 - typescript: 타입스크립트 라이브러리
 - @types/node: 자바스크립트 런타임 노드의 타입이 정의된 타입 정의 파일
 - @types/react: 리액트의 타입이 정의된 타입 정의 파일
 - @types/react-dom: react-dom의 타입이 정의된 타입 정의 파일
```Bash
# 리액트 프로젝트 생성
$ npx create-react-app my-app

# 타입스크립트 라이브러리 설치
$ npm install --save-dev typescript @types/node @types/react @types/react-dom
```

 - tsconfig.json
    - 타입스크립트 프로젝트를 컴파일 하기 위한 여러 가지 옵션을 설정할 수 있는 파일
    - [타입스크립트 공식 문서](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html)
    - ./src/App.js -> ./src/App.tsx
    - ./src/App.test.js -> ./src/App.test.tsx
    - ./src/index.js -> ./src/index.tsx
    - ./src/reportWebVitals.js -> ./src/reportWebVitals.ts
    - ./src/setupTests.js -> ./src/setupTests.ts
```JSON
{
    "compilerOptions": {
        "target": "es5",
        "lib": [
            "dom",
            "dom.iterable",
            "esnext"
        ],
        "allowJs": true,
        "skipLibCheck": true,
        "esModuleInterop": true,
        "allowSyntheticDefaultImports": true,
        "strict": true,
        "forceConsistentCasingInFileNames": true,
        "noFallthroughCasesInSwitch": true,
        "module": "esnext",
        "moduleResolution": "node",
        "resolveJsonModule": true,
        "isolatedModules": true,
        "noEmit": true,
        "jsx": "react-jsx"
    },
    "include": [
        "src"
    ]
}
```

 - ./src/custom.d.ts
    - d.ts 파일은 탕비 정의 파일로 타입스크립트가 안에서 사용할 특정 타입들을 정의할 때 사용한다.
```TS
declare module '*.svg' {
    export const ReactComponent: React.FunctionComponent<React.SVGProps<SVGSVGElement> & { title?: string }>;

    const src: string;
    export default src;
}
```
 - ./src/reportWebVitals.ts
```TS
import { ReportHandler } from 'web-vitals';

const reportWebVitals = (onPerfEntry?: ReportHandler) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};

export default reportWebVitals;
```

 - ./src/index.tsx
```tsx
const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
..
```

<br/>

### 3.1.2 create-react-app 타입스크립트 템플릿 사용

create-react-app으로 리액트 프로젝트를 만들고, 하나씩 타입스크립트를 설정할 수 있다.  
하지만, 이러한 방법은 너무 복잡하다.  
때문에, create-react-app에서는 타입스크립트가 적용된 리액트 프로젝트를 생성할 수 있는 템플릿 옵션을 제공한다.  
```Bash
$ npx create-react-app my-app-typescript --template=typescript
$ npm start
```

<br/>

## 3.2 스타일링

리액트는 웹 애플리케이션 개발에 사용되는 라이브러리로 스타일링에 CSS를 사용할 수 있다.  
또한, 자바스크립트에서 CSS 파일을 불러오거나 자바스크립트 안에서 스타일링을 하는 데 CSS-in-JS 기법을 사용할 수 있다.  

<br/>

### 3.2.1 CSS와 Link 태그

create-react-app으로 만든 프로젝트의 public 폴더는 %PUBLIC_URL%로 접근할 수 있다.  
리액트에서는 HTML 태그에 class 대신 className을 사용하여 클래스를 지정한다.  
그 이유로는 리액트는 자바스크립트 라이브러리이고, 자바스크립트에는 이미 class라는 키워드가 존재한다.  

<br/>

### 3.2.2 CSS와 import

리액트는 보통의 웹 페이지 개발과 달리 컴포넌트를 중심으로 개발한다.  
때문에, <link/> 태그를 사용하여 CSS를 한 곳에서 관리하게 되면, 어떤 컴포넌트에서 어떤 스타일을 활용하고 있는지 빠르게 이해하기 어렵다.  
그래서, 리액트에서는 CSS 파일을 리액트 컴포넌트 파일에서 import 하는 방식으로 스타일도 컴포넌트 중심으로 설계할 수 있도록 하고 있다.  

```JS
// App.tsx
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        ..
      </header>
    </div>
  );
}

// App.css
.App-header {
  background-color: #282c34;
  min-height: 100vh;
  ..
}
```

<br/>

### 3.2.3 CSS-in-JS (Emotion)

보통 리액트는 컴포넌트를 기반으로 개발되어 컴포넌트별로 CSS 파일을 갖는 형식으로 스타일을 관리한다.  
하지만, 이렇게 각각의 컴포넌트에서 CSS를 분리하여 관리하다 보면, CSS의 클래스 명이 중복되어 의도치 않은 스타일이 적용될 수 있다.  
이러한 문제를 해결하기 위해 CSS-in-JS 방법론이 탄생하였고, 리액트에서는 styled-components, Emotion 등과 같은 라이브러리를 통해 이를 적용할 수 있다.  
 - 클래스 명 버그 해결
    - 클래스 명의 중복, 겹침 또는 철자 오류와 같은 문제를 해결한다.
 - 보다 쉬운 CSS 관리
    - CSS-in-JS는 모든 스타일이 특정 컴포넌트에 연결되기 때문에 보다 명확히 사용되는 스타일을 알 수 있으며, 모든 스타일이 특정 컴포넌트에 연결되어 있기 때문에 사용되지 않은 불필요한 스타일을 쉽게 제거할 수 있다.
 - 간단한 동적 스타일 적용
    - CSS-in-JS는 동적인 스타일을 관리하기 위해 여러 클래스를 만들 필요가 없으며 컴포넌트의 상태에 따라 쉽고 직관적으로 동적 스타일을 적용할 수 있다.
 - CSS 자동 구성
    - CSS-in-JS 라이브러리인 styled-components 또는 Emotion을 사용하면 페이지에 렌더링되는 컴포넌트를 추적하여 해당 스타일을 완전히 자동으로 추가한다. 또한 코드 분할시 사용자가 필요한 최소한의 코드를 자동으로 추가한다.
```Bash
$ npx create-react-app my-app-css-in-js --template=typescript
$ cd my-app-css-in-js
$ npm install --save @emotion/react @emotion/styled
```

<br/>

## 3.3 절대 경로로 컴포넌트 추가

리액트 프로젝트 개발 시 수 많은 리액트 컴포넌트를 제작하고, 제작한 컴포넌트를 블록을 조합하듯 하여 페이지를 제작하게 된다.  
이때, 보통은 상대 경로를 사용하여 부러와 사용할 수 있다.  
하지만, 프로젝트가 커지고 수 많은 컴포넌트들이 추가되어 폴더 구조가 복잡해지면, 상대 경로 추가 방식은 어떤 경로를 지정하고 있는지 명확하게 파악하기 어려워진다.  
이러한 문제는 탕비스크립트의 설정으로 간단히 해결할 수 있다.  

```Bash
$ npx create-react-app my-app-root-import --template=typescript
```

<br/>
 - tsconfig.json
    - baseUrl을 설정하면, src 폴더를 기본으로 하는 절대 경로로 컴포넌트를 추가할 수 있다.
    - 물론, 상대 경로로 컴포넌트를 추가하는 방법도 사용 가능하다.
```JSON
{
  "compilerOptions": {
    ..
    "jsx": "react-jsx",
    "baseUrl": "src"
  }
}
```

<br/>

## 3.4 Prettier

Prettier는 코드 포맷터로 Javascript, CSS, JSON 등을 지원한다.  
Prettier는 미리 약속한 코드 스타일에 맞춰 자동으로 코드의 형식을 수정해 주는 도구로, 협업 시 여러 개발자들의 코드 스타일을 맞추는 데 큰 도움을 준다.  
Prettier는 혼자서 개발할 때에는 큰 힘을 발휘하지 않지만, 여러 명이 동시에 같은 프로젝트를 수행할 때에 일관된 코드 스타일을 유지할 수 있도록 도와주기 때문에 협업에서는 필수 툴로 자리 잡고 있다.  
 - [Prettier 공식 사이트](https://prettier.io/)

<br/>

### 3.4.1 Prettier 설치

```Bash
$ npm create-react-app my-app-prettier --template=typescript
$ npm install --save-dev prettier
```

<br/>

### 3.4.2 Prettier 설정

프로젝트 최상위 폴더에 '.prettierrc.js' 파일을 통해 Prettier 설정을 지정할 수 있다.
 - .prettierrc.js
    - singleQuote: 싱글쿼트(')를 주로 사용하도록 설정)
    - trailingComma: 콤마(,)를 추가할 수 있다면, 콤마를 추가하도록 설정
    - printWidth: 한 줄에 작성할 수 있는 최대 코드 문자 수를 설정
```JS
module.exports = {
  singleQuote: true,
  trailingComma: 'all',
  printWidth: 100,
}
```

<br/>

### 3.4.3 Prettier 실행

package.json 파일에 Prettier 실행 명령어를 설정한다.  

 - package.json
    - format: Prettier를 check 옵션과 함께 실행하여 설정한 내용에 위반되는 내용이 있는지 검사한다.
    - format:fix: Prettier를 write 옵션과 함께 사용하여 잘못된 내용을 설정한 내용에 맞게 자동으로 수정해준다.
```JSON
{
  ...
  "script": {
    ..
    "format": "prettier --check ./src",
    "format:fix": "prettier --write ./src"
  },
}
```
 - Prettier 실행
    - npm run 명령어로 script에 정의된 prettier 실행 명령어를 수행한다.
    - format으로 위반 내용을 확인하고, format:fix로 위반 내용을 수정한다.
    - 마지막으로, format을 한 번더 수행하여 모든 문제가 잘 해결된 것을 확인한다.
```Bash
# 위반 내용 확인
$ npm run format

# 위반 내용 수정
$ npm run format:fix
```

<br/>

## 3.5 ESLint

ESLint는 ES(ECMAScript)와 Lint(에러 코드 표식)의 합성어로, 자바스크립트의 코드를 분석하고 잠재적인 오류나 버그를 찾는 데 도움을 주는 정적 분석 툴이다.  
여러 개발자들이 하나의 소스 코드를 수정하는 협업 환경에서 ESLint는 소스 코드를 분석하고 오류나 버그의 가능서을 지적하거나 소스 코드의 스타일을 일관성 있게 관리해주어 Prettier와 함께 자주 사용된다.  
 - ESLint는 정적 소스 코드 분석 툴로 간단한 문법적 오류나 복잡한 코드 스타일에 의해 발생할 가능성이 높은 버그만을 찾을 수 있다.
 - 즉, 프로그램이 실행 중에 발생하는 버그는 알 수 없으며 비즈니스 로직에서 문제점을 찾을 수 없다.
 - 때문에, ESLint는 보조적인 툴로써 사용하도록 한다.

<br/>

### 3.5.1 ESLint 설치

```Bash
$ npx create-react-app my-app-eslint --template=typescript
$ npm install eslint --save-dev
```

<br/>

### 3.5.2 ESLint 설정

```Bash
$ npx eslint --init

# 1. ESLint를 설정하기 위해 필요한 라이브러리 설치 여부: y
You can also run this command directly using 'npm init @eslint/config'.
Need to install the following packages:
  @eslint/create-config@0.4.5
Ok to proceed? (y) y

# 2. ESLint를 어떻게 사용할 것인지 여부: To check syntax and find problems
# 문제점을 찾는 것과 잘못된 점을 고치는 스크립트를 따로 작성할 것이기 때문에 해당 옵션으로 선택한다.
? How would you like to use ESLint? ...
  To check syntax only
> To check syntax and find problems
  To check syntax, find problems, and enforce code style

# 3. ESLint를 사용하는 자바스크립트 프로젝트에서 모듈 시스템 방식 여부: JavaScript modules
# 리액트는 기본적으로 자바스크립트 모듈 방식을 사용한다.
? What type of modules does your project use? ... 
> JavaScript modules (import/export)
  CommonJS (require/exports)
  None of these

# 4. ESLint를 사용할 프레임워크 여부: React
? Which framework does your project use? ...       
> React
  Vue.js
  None of these

# 5. 타입스크립트 사용 여부: Yes
? Does your project use TypeScript? » No / Yes

# 6. 현재 프로젝트가 어떤 환경에서 실행되는지: Browser
# 리액트 프로젝트로 웹 브라우저에 실행되므로 Browser를 선택한다.
? Where does your code run? ...  (Press <space> to select, <a> to toggle all, <i> to invert selection)
√ Browser
√ Node

# 7. ESLint 구성 파일 형식: JavaScript
# .eslintrc.js 파일로 ESLint의 옵션을 설정할 수 있다.
? What format do you want your config file to be in? ... 
> JavaScript
  YAML
  JSON

# 8. 필요한 라이브러리 설치 여부: Yes
# 지금까지 설정한 내용을 정상적으로 적용하기 위해서는 해당 라이브러리들이 필요하므로 Yes로 설치를 진행한다.
The config that you`ve selected requires the following dependencies:

@typescript-eslint/eslint-plugin@latest eslint-plugin-react@latest @typescript-eslint/parser@latest
? Would you like to install them now? » No / Yes

# 9. 패키지 매니저 사용 여부: npm
# 과거에 npm의 단점으로 yarn을 사용하는 경우가 많았지만, npm이 업데이트되면서 yarn과 성능 차이가 거의 없다.
? Which package manager do you want to use? ...
> npm
  yarn
  pnpm
```

<br/>

 - .eslintrc.js
    - ESLint: https://eslint.org/docs/latest/rules/
    - 타입스크립트: https://github.com/typescript-eslint/typescript-eslint/tree/main/packages/eslint-plugin#supported-rules
    - extends를 살펴보면, ESLint, 리액트와 타입스크립트의 추천 룰을 사용하는 것을 확인할 수 있다.
    - 만약, ESLint와 타입스크립트 검사 룰을 변경하고 싶다면, rules 옵션에 필요한 내용을 추가하면 된다.
    - 마지막으로, ESLint에 리액트 버전을 알려줄 필요가 있다. 또한, react/react-in-jsx-scope 규칙의 사용을 중지시킬 필요가 있다.
    - .exlintrc.js 파일에 settings 옵션으로 react 버전을 명시하고, rules에 react/react-in-jsx-scope 규칙을 중지한다.
      - 기존 리액트에서 JSX 파일안에 import React from 'react'를 항상 사용하여야 했다.
      - 하지만, 리액트 17 버전부터 해당 규칙이 사라져서 사용하지 않도록 할 필요가 있다. (react/react-in-jsx-scope)
```JS
module.exports = {
  settings: {
    react: {
      version: "detect",
    },
  },
  env: {
    browser: true,
    es2021: true,
  },
  extends: [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:react/recommended",
  ],
  overrides: [
    {
      env: {
        node: true,
      },
      files: [".eslintrc.{js,cjs}"],
      parserOptions: {
        sourceType: "script",
      },
    },
  ],
  parser: "@typescript-eslint/parser",
  parserOptions: {
    ecmaVersion: "latest",
    sourceType: "module",
  },
  plugins: ["@typescript-eslint", "react"],
  rules: {
    "react/react-in-jsx-scope": "off",
  },
};
```

<br/>

### 3.5.3 ESLint 실행

package.json 파일에 ESLint 실행 명령어를 설정한다.  

 - package.json
    - lint: ESLint를 검사한다.
    - lint:fix: ESLint 검사하고, 설정한 룰을 기반으로 자동으로 수정하도록 한다.
```JSON
{
  ...
  "script": {
    ..
    "lint": "eslint ./src",
    "lint:fix": "eslint --fix ./src"
  },
}
```

<br/>

 - ESLint 실행
    - npm run 명령어로 script에 정의된 prettier 실행 명령어를 수행한다.
    - format으로 위반 내용을 확인하고, format:fix로 위반 내용을 수정한다.
    - 마지막으로, format을 한 번더 수행하여 모든 문제가 잘 해결된 것을 확인한다.
```Bash
# 위반 내용 확인
$ npm run lint

# 위반 내용 수정
$ npm run lint:fix
```