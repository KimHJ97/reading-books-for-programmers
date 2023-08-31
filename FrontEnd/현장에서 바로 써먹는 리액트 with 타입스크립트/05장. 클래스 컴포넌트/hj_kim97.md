# 05. 클래스 컴포넌트

## 5.1 클래스 컴포넌트

리액트는 16.8 버전 이전까지 함수 컴포넌트에서 컴포넌트의 상태를 관리하는 데 State를 사용할 수 없었다.  
때문에, 버전 16.8 이전까지 기본적으로 클래스 컴포넌트를 기본 컴포넌트로 사용되었다.  
최근에는 함수 컴포넌트를 많이 사용하지만 리액트 버전 16.8이 나오기 전까지 긴 시간 동안 이미 많은 리액트 웹 애플리케이션이 클래스 컴포넌트로 개발되었다.  
때문에, 클래스 컴포넌트를 다루는 방법에 대해서도 이해하고 있어야 한다.  
 - 리액트 훅 도입 동기: https://ko.reactjs.org/docs/hooks-intro.html#motivation
 - 리액트 훅이란 useState, useEffect, useContext 등을 사용하여 함수 컴포넌트에서도 클래스 컴포넌트의 상태 관리, 컴포넌트의 생명 주기를 사용할 수 있게 해주는 방법을 말한다.

<br/>

## 5.2 프로젝트 준비

```Bash
# 프로젝트 생성
$ npx create-react-app class-counter --template=typescript

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

# 모든 설정 파일을 생성하고 나서 실행: 모든 파일들을 Prettier와 ESLint의 룰에 맞게 초기화
$ npm run format:fix
$ npm run lint:fix
$ npm run format
$ npm run lint
$ npm start

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

 - .prettierrc.js
```JS
module.exports = {
  singleQuote: true,
  trailingComma: 'all',
  printWidth: 100,
};
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
    'react/react-in-jsx-scope': 'off',
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

## 5.3 소스 코드

 - 함수형 컴포넌트: export const 컴포넌트명 = (Props 데이터) => { .. };
 - 클래스형 컴포넌트: export class 컴포넌트명 extends Component<Props 제네릭, State 제네릭> { render() { .. } }
    - 클래스 컴포넌트를 생성하기 위해서는 Component 클래스를 상속받아 새로운 클래스를 생성한다.
```TS
// 클래스형 컴포넌트 (Props, State 미사용시)
export class Button extends Component { .. }

// 클래스형 컴포넌트 (Props만 사용)
export class Button extends Component<Props> { .. }

// 클래스형 컴포넌트 (State만 사용)
export class Button extends Component<Record<string, never>, State> { .. }

// 클래스형 컴포넌트 (Props, State 사용)
export class Button extends Component<Props, State> { .. }
```

<br/>

 - 코드 변경
    - 함수형 컴포넌트는 JSX를 사용하여 반환값으로 화면에 표시될 부분을 반환한다. 이때 부모 컴포넌트로부터 전달받는 데이터인 Props를 함수의 매개 변수를 통해 전달받게 된다.
    - 반면 클래스형 컴포넌트는 리액트의 라이프사이클 함수인 render 함수에서 화면에 표시될 부분을 반환해야 한다.
    - 생성자 함수는 State를 초기화하는 데 활용된다.
        - 생성자 함수를 사용할 때에는 super(props)를 통해 상속받은 클래스(Component)에 Props를 전달해 주어야 한다.
    - useState 훅을 사용하는 함수 컴포넌트와 달리, 클래스 컴포넌트에서 State 변수에 접근하기 위해서는 this.state를 사용해야 한다.
        - 또한, State를 변경하기 위해서는 this.setState 함수를 사용해야 한다.
```TS
// Before (Button, Label 컴포넌트)
export const Button = ({ label, onClick }: Props) => {
  return <Container onClick={onClick}>{label}</Container>;
};

export const Label = ({ data }: Props) => {
  return <Container>{data}</Container>;
};

// After (Button, Label 컴포넌트)
export class Button extends Component<Props> {
  render() {
    const { label, onClick } = this.props;
    return <Container onClick={onClick}>{label}</Container>;
  }
}

export class Label extends Component<Props> {
  render() {
    const { data } = this.props;
    return <Container>{data}</Container>;
  }
}

// Before (App 컴포넌트)
function App() {
  const [counter, setCounter] = useState(0);

  const sub = () => {
    setCounter(counter - 1);
  };
  const add = () => {
    setCounter(counter + 1);
  };

  return (
    <Container>
      <Title>Counter App</Title>
      <Contents>
        <Button label="-" onClick={sub} />
        <Label data={counter} />
        <Button label="+" onClick={add} />
      </Contents>
    </Container>
  );
}

// After (App 컴포넌트)
export class App extends Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      counter: 0,
    };
  }

  private sub = () => {
    const { counter } = this.state;
    this.setState({
      counter: counter - 1,
    });
  };

  private add = () => {
    const { counter } = this.state;
    this.setState({
      counter: counter + 1,
    });
  };

  render() {
    const { counter } = this.state;

    return (
      <Container>
        <Title>Counter App</Title>
        <Contents>
          <Button label="-" onClick={this.sub} />
          <Label data={counter} />
          <Button label="+" onClick={this.add} />
        </Contents>
      </Container>
    );
  }
}
```

<br/>

## 5.4 라이프사이클 함수

클래스 컴포넌트는 함수 컴포넌트와 달리 라이프사이클 함수들을 가지고 있다.  
이 라이프사이클 함수를 잘 이해하면, 클래스 컴포넌트를 좀 더 효율적으로 활용할 수 있다.  

### constructor 함수

클래스 컴포넌트에서 State를 사용하지 않아 State의 초깃값을 설정할 필요가 없다면, 생성자 함수도 생략이 가능하다.  
생성자 함수를 사용할 때에는 반드시 super(props) 함수를 호출하여 상속받은 클래스의 생성자를 호출해야 한다.  
 - 생성자 함수는 해당 클래스 컴포넌트가 생성될 떄에 한 번만 호출된다.

<br/>

### render 함수

render 함수는 클래스 컴포넌트의 화면 표시 부분을 정의하는 데 사용한다.  
즉, render 함수의 반환값이 화면에 표시되게 된다.  
 - render 함수는 Props 값이 변경되거나 this.setState를 사용하여 State의 값이 변경되어 화면을 갱신할 필요가 있을 때마다 호출된다.
    - render 함수 안에서 this.setState를 사용하여 State 값을 변경하면 무한 루프에 빠질 수 있다.

<br/>

### getDerivedStateFromProps 함수

getDerivedStateFromProps 함수는 부모 컴포넌트로부터 받은 Props와 State를 동기화할 때 사용된다.  
부모 컴포넌트로부터 받은 Props로 State의 특정값을 설정하거나 State 값이 Props에 의존하여 결정될 때 getDerivedStateFromProps 함수를 사용한다.  
쉽게, Props의 값에 따라 State 값을 설정하고 싶을 때 사용할 수 있다. Props가 변경될 때마다 호출되므로 변경된 값에 따라 State를 지정할 수 있다.  
만약, 부모 컴포넌트로부터 전달받은 Props에 의해 State 값을 변경할 필요가 없는 경우에는 "null"을 반환하면 된다.
 - getDerivedStateFromProps 함수는 컴포넌트가 생성될 때 Props에 의해 State 값을 결정해야 하므로 한 번 호출되며,
 - 이후에 Props와 State를 동기화해야 하므로 Props가 변경될 때마다 호출된다.
```TS
static getDerivedStateFromProps(nextProps: Props, prevState: State) {
  if (nextProps.id !== prevState.id) {
    return { type: "admin"};
  }

  return null;
}
```

<br/>

### componentDidMount 함수

클래스 컴포넌트가 처음으로 화면에 표시된 후 componentDidMount 함수가 호출된다.  
render 함수와 다르게 componentDidMount 함수는 화면 렌더링 이후 단 한 번만 호출된다.  
때문에, Ajax를 통해 서버로부터 전달받은 데이터를 this.setState를 사용하여 State에 설정하기에 가장 적합하다.
 - componentDidMount 함수는 초기 렌더링 이후 단 한번만 호출된다.
 - Props 값이 변경되거나, State 값이 변경되어도 두 번 다시 호출되지 않는다.

<br/>

### shouldComponentUpdate 함수

클래스 컴포넌트는 기본적으로 Props가 변경되거나 State가 변경되면 화면을 다시 그리기 위해 리렌더링을 하게 된다.  
하지만, 특정 이유로 Props 또는 State가 변경되어도 화면을 변경하고 싶지 않은 경우가 발생할 수 있다.  
이러한 경우 shouldComponentUpdate 함수를 사용하여 컴포넌트의 리렌더링을 제어할 수 있다.  
해당 함수에서 false를 반환하면, 컴포넌트의 리렌더링을 수행하지 않도록 막을 수 있다.  
shouldComponentUpdate 함수를 사용하여 데이터를 비교하고 불필요한 리렌더링을 제어한다면, 좀 더 성능 좋은 앱을 제작할 수 있다.  
 - shouldComponentUpdate 함수는 Props 혹은 State 값이 변경될 때마다 호출되며, 렌더링 전에 호출된다.
```TS
shouldComponentUpdate(nextProps: Props, nextState: State) {
  console.log('shouldComponentUpdate');
  console.log('nextProps: ', nextProps);
  console.log('nextState: ', nextState);
  return false;
}
```

<br/>

### getSnapshotBeforeUpdate 함수

Props나 State가 변경되어 화면을 다시 그리기 위해 render 함수가 호출된 후 render 함수의 반환값이 실제로 화면에 반영되기 바로 직전에 getDerivedStateFromProps 함수가 호출된다.  
이 함수에서 반환하는 값은 componentDidUpdate 함수의 세 번째 매개 변수로 전달된다.  
해당 라이프사이클 함수는 많이 활용되지는 않지만, 화면을 갱신하는 동안 수동으로 스크롤 위치를 고정해야 하는 경우 등에 사용될 수 있다.  
 - getSnapshotBeforeUpdate 함수는 Props 혹은 State 값이 변경될 때마다 호출된다. 렌더링 이후에 호출된다.
 - 해당 함수의 반환값이 없거나, 해당 함수 선언 후 componentDidUpdate 함수를 선언하지 않는 경우 경고(Warning)가 발생한다.

<br>

### componentDidUpdate 함수

componentDidMount 함수는 컴포넌트가 처음 화면에 표시된 후 실행되고 두 번 다시 호출되지 않는 함수이다.  
반대로 componentDidUpdate 함수는 컴포넌트가 처음 화면에 표시될 때에는 실행되지 않고, Props 또는 State가 변경되어 화면이 갱신될 때마다 render 함수가 호출된 후 매번 호출되는 함수이다.  
해당 함수는 잘 활용되지는 않지만, getSnapshotBeforeUpdate 함수와 함께 사용하여 스크롤을 수동으로 고정시킬 때 활용되기도 한다.
 - getSnapshotBeforeUpdate 함수는 Props 혹은 State 값이 변경될 때마다 호출된다. 렌더링 이후에 호출된다.
 - 리렌더링시 마다 호출되므로 해당 함수 안에서 this.setState를 사용하여 State 값을 변경하면 무한 루프에 빠질 수 있다.

<br/>

### componentWillUnmount 함수

componentWillUnmount 함수는 해당 컴포넌트가 화면에서 완전히 사라진 후 호출되는 함수로 보통 componentDidMount 함수에서 연동한 자바스크립트 라이브러리를 해제하거나 setTimeout, setInterval 등의 타이머를 clearTimeout, clearInterval을 사용하여 해제할 때에 사용한다.  
componentWillUnmount 함수는 클래스 컴포넌트가 화면에서 완전히 사라진 후 호출되므로 컴포넌트의 State 값을 변경하기 위한 this.setState를 호출하면, 갱신하고자 하는 컴포넌트가 사라진 후이기 때문에 경고가 발생한다.
 - componentWillUnmount 함수는 해당 컴포넌트가 화면에서 완전히 사라진 후 호출된다.


<br/>

### componentDidCatch 함수

리액트는 자바스크립트로 비즈니스 로직에서 에러의 예외 처리로 try-catch문을 사용할 수 있다.  
하지만, render 함수의 JSX 문법을 사용하는 부분에서 에러가 발생하는 경우 try-catch문을 사용하여 예외를 처리할 수 없다.  
이와 같이 render 함수의 JSX 부분에서 발생하는 에러를 예외 처리할 수 있게 도와주는 라이프사이클 함수가 componentDidCatch 함수이다.  

<br/>

render 함수의 JSX 부분에서 에러가 발생하면, componentDidCatch 함수가 실행된다.  
이때 State를 사용하여 에러가 발생했을 때에 자식 컴포넌트를 표시하지 않게 하거나 에러 화면을 표시함으로써 사용자 경험을 개선할 수 있다.
```TS
interface State {
    ..
    readonly error: boolean;
}

class App extends Component<Props, State> {
    constructor(props: Props) {
        super(props);

        this.state = {
            error: false,
        };
    }

    ..

    render() {
        const { ..., error } = this.state;

        return (
            <Container>
                {!error && (
                    <Contents>
                        ..
                    <Contents>
                )}
            </Container>
        );

        componentDidCatch(error: Error, info: React.ErrorInfo) {
            this.setState({
                error: true,
            });
        }
    }
}
```

<br/>

### 호출 순서

 - 컴포넌트가 생성될 때
    - constructor -> getDerivedStateFromProps -> render -> componentDidMount
    - 생성자(constructor)에서 Props, State 초기값 설정, getDerivedStateFromProps에서 Props와 State 동기화, componentDidMount에서 외부 API를 통한 State 초깃값 설정
 - 컴포넌트의 Props가 변경될 때
    - getDerivedStateFromProps -> shouldComponentUpdate -> render -> getSnapshotBeforeUpdate -> componentDidUpdate
    - getDerivedStateFromProps에서 Props와 State 동기화, shouldComponentUpdate에서 리렌더링 여부 설정
 - 컴포넌트의 State가 변경될 때
    - shouldComponentUpdate -> render -> getSnapshotBeforeUpdate -> componentDidUpdate
    - shouldComponentUpdate에서 리렌더링 여부 설정
 - 컴포넌트의 렌더링 중 에러가 발생할 때
    - componentDidCatch
 - 컴포넌트가 화면에서 제거될 때
    - componentWillUnmount

```JS
export class App extends Component<Props, State> {
  constructor(props: Props) {
    super(props);

    this.state = {
      ..
    };
  }

  render() {
    const { .. } = this.state;

    return (
      <Container>
        ..
      </Container>
    );
  }

  static getDerivedStateFromProps(nextProps: Props, prevState: State) {
    console.log('getDerivedStateFromProps');
    console.log('nextProps: ', nextProps);
    console.log('prevState: ', prevState);

    return null;
  }

  componentDidMount() {
    console.log('componentDidMount');
  }

  getSnapshotBeforeUpdate(prevProps: Props, prevState: State) {
    console.log('getSnapshotBeforeUpdate');
    console.log('prevProps: ', prevProps);
    console.log('prevState: ', prevState);

    return {
      testData: true,
    };
  }

  componentDidUpdate(prevProps: Props, prevState: State, snapshot: IScriptSnapshot) {
    console.log('componentDidUpdate');
    console.log('prevProps: ', prevProps);
    console.log('prevState: ', prevState);
    console.log('snapshot: ', snapshot);
  }

  shouldComponentUpdate(nextProps: Props, nextState: State) {
    console.log('shouldComponentUpdate');
    console.log('nextProps: ', nextProps);
    console.log('nextState: ', nextState);
    return false;
  }

  componentWillUnmount() {
    console.log('componentWillUnmount');
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.log('componentDidCatch');
    console.log('error: ', error);
    console.log('info: ', info);
    // this.setState({
    //   error: true,
    // });
  }
```