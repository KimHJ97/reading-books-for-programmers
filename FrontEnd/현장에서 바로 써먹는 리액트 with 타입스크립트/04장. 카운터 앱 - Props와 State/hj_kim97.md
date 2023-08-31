# 04. 카운터 앱 - Props와 State

## 4.1 Props와 State

리액트에서는 데이터를 다루는 방법으로 Props와 State, Context를 제공한다.  

<br/>

Props는 Properties의 약자로 '특성'이라는 의미를 가지고 있다.  
Props는 리액트 컴포넌트의 특성을 나타내며, 이 특성을 통해 부모 컴포넌트가 자식 컴포넌트에 데이터를 전달할 수 있다.  
부모 컴포넌트로부터 전달받는 데이터이고 해당 컴포넌트의 특성이므로 자식 컴포넌트에서는 변경이 불가능하다.  

<br/>

State는 '상태'라는 의미를 가지고 있다.  
State는 리액트 컴포넌트의 현재 상태를 의미하며, 이 컴포넌트 상태는 변경이 가능하다.  
State는 한 컴포넌트 안에서 유동적인 데이터를 다룰 때에 사용되며, 컴포넌트 안에서 데이터를 변경할 수 있다.  
즉, State는 한 컴포넌트의 상태를 나타낸다.  

<br/>

## 4.2 프로젝트 준비

 - CRA를 이용하여 리액트 프로젝트를 생성한다.
 - 이후 CSS-in-JS 라이브러리 Emotion 설치와 소스 코드 포맷 및 잠재적인 오류를 찾을 수 있는 Prettier와 ESLint를 설치한다.
```Bash
# 프로젝트 생성
$ npx create-react-app counter --template=typescript

# Emotion, Prettier, ESLint 설치 설치
$ npm install --save @emotion/react @emotion/styled
$ npm install --save-dev prettier eslint

# ESLint 설정 초기화
$ npx eslint --init
You can also run this command directly using 'npm init @eslint/config'.
√ How would you like to use ESLint? · problems    
√ What type of modules does your project use? · esm
√ Which framework does your project use? · react
√ Does your project use TypeScript? · No / Yes
√ Where does your code run? · browser
√ What format do you want your config file to be in? · JavaScript
@typescript-eslint/eslint-plugin@latest eslint-plugin-react@latest @typescript-eslint/parser@latest
√ Would you like to install them now? · No / Yes
√ Which package manager do you want to use? · npm
```

<br/>

 - tsconfig.json
    - baseUrl 옵션
```JSON
{
  "compilerOptions": {
    ..
    "jsx": "react-jsx",
    "baseUrl": "src"
  },
}
```

<br/>

 - .eslintrc.js
    - settings 옵션: 리액트 버전 명시
    - rules 옵션: 필요없는 React 문법 룰 제거
```JS
module.exports = {
  settings: {
    react: {
      version: "detect",
    },
  },
  ..
  rules: {
    "react/react-in-jsx-scope": "off",
  },
};
```

<br/>

 - package.json
    - ESLint와 Prettier 실행 명령 스크립트 추가
```JSON
{
  ..
  "scripts": {
    ..
    "format": "prettier --check ./src",
    "format:fix": "prettier --write ./src",
    "lint": "eslint ./src",
    "lint:fix": "eslint --fix ./src"
  },
}
```

<br/>

## 4.3 카운터 앱 - 소스 코드

 - https://github.com/dev-yakuza/react_with_typescript_book_examples/tree/main/ch4.counter

<br/>

### State

State는 리액트 컴포넌트의 현재 상태를 의미한다.  
즉, State는 한 컴포넌트 안에서 유동적인 데이터를 다루거나 컴포넌트 안에서 데이터가 변경되고 그 내용이 화면에 반영되어야 할 때에 사용한다.  
카운터 앱에서는 더하기, 빼기 버튼을 클릭했을 때에 카운터 값이 변경되고, 변경된 값이 화면에 표시돼야 한다.  
즉, 화면에 표시되는 숫자가 State에 의해 관리되어야 하는 변수이다.

 - const 배열 = useState(데이터 초기값);
    - 배열[0]: 데이터 초기값이 들어간 변수
    - 배열[1]: 데이터를 수정할 수 있는 set 함수
    - const [변수명, set함수명] = useState(데이터 초기값);
    - 실무에서는 반환된 결과값을 자바스크립트의 구조 분해 할당 문법을 통해 변수와 set 함수를 할당하여 사용한다.
```JS
const [counter, setCounter] = useState(0);

const sub = () => {
  setCounter(counter - 1);
};

const add = () => {
  setCounter(counter + 1);
};

return (
  ..
  <Button onClick={sub}>-<Button>
  <Label>{counter}</Label>
  <Button onClick={add}>+<Button>
);
```

<br/>

### Props

리액트는 컴포넌트를 만들어 조립하듯이 개발을 하게 된다.  
Button과 Label을 별도의 파일로 분리하여 사용하도록 한다.  
이러한 경우 화면은 App.tsx에서 보여지고 해당 화면에 카운터 숫자를 보여줄 상태(State)를 관리하게 된다.  
Button과 Label에는 부모 컴포넌트에 상태를 Props로 전달받을 수 있지만 부모 컴포넌트에 상태를 직접 조작할 수 없다.  
때문에, Label 컴포넌트에서는 Props로 부모 컴포넌트의 카운터 숫자를 받아 보여주는 역할을 하고,  
Button 컴포넌트에서는 Props로 부모 컴포넌트의 함수를 받는다. 이 함수는 카운터 숫자를 조작하는 함수이다.  
Button 컴포넌트에서 부모 컴포넌트의 상태(State)를 직접 조작할 수 없으니, 부모 컴포넌트의 함수를 Props로 받아 해당 함수를 호출하여 조작한다.  
 - Label: 부모 컴포넌트의 상태(State) 값을 Props로 전달받는다.
 - Button: 부모 컴포넌트의 함수를 Props로 전달받는다. 해당 컴포넌트 내부에 onClick시 해당 Props로 전달받은 함수를 호출한다. 이로서 부모 컴포넌트의 상태(State) 값을 변경할 수 있다.
 - export const 컴포넌트명 = (Props 데이터) => { .. };
    - 전달받은 Props 데이터는 객체 형태로 가지게 되며, props.onClick, props.label과 같이 접근하여 사용할 수 있다.
    - 부모 컴포넌트로부터 전달받는 매개 변수인 Props 데이터는 단순한 변수이므로 변수명은 어떤 이름을 사용해도 상관없다.
    - 실무에서는 객체에 접근하는 방식을 사용하지 않고, 구조 분해 할당을 사용한다.
```TS
// Button
interface Props {
  readonly label: string;
  readonly onClick?: () => void;
}

// export const Button = (props: Props) => { .. }; // Props 객체에 접근하는 방식
export const Button = ({ label, onClick }: Props) => {
  return <Container onClick={onClick}>{label}</Container>;
};

// Label
interface Props {
  readonly data: number;
}

export const Label = ({ data }: Props) => {
  return <Container>{data}</Container>;
};
```

<br/>

### 정리

Props는 부모 컴포넌트로부터 자식 컴포넌트로 전달되는 데이터이고, State는 한 컴포넌트 안에서 유동적인 데이터를 다룰 때에 사용한다.  
 - const 배열 = useState(데이터 초기값);
    - 배열[0]: 데이터 초기값이 들어간 변수
    - 배열[1]: 데이터를 수정할 수 있는 set 함수
    - const [변수명, set함수명] = useState(데이터 초기값);
 - export const 컴포넌트명 = (Props 데이터) => { .. };
    - Props 데이터 접근(매개변수를 props로 받은 경우): props.변수명
    - Props 데이터 접근(구조 분해 할당): 변수명