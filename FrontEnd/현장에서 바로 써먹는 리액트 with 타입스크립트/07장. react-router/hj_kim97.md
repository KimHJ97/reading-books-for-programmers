# 07. react-router

## 7.1 react-router

리액트는 웹 애플리케이션에서 UI를 만들기 위한 자바스크립트 라이브러리이다.  
리액트는 프레임워크가 아닌 라이브러리 성향을 갖고 있어 기본적으로 페이지 이동에 관한 기능을 제공하지 않는다.  
때문에, 리액트를 사용하는 웹 애플리케이션에서 페이지 이동과 같이 UI와 관계없는 기능을 사용하고 싶은 경우 외부 라이브러리를 이용해야 한다.  

<br/>

리액트에서 사용자가 요청한 URL을 이용하여 특정 컴포넌트를 표시하도록 하기 위해서는 react-router라는 외부 라이브러리를 사용해야 한다.  
react-router를 사용하면, 리액트에서 URL에 해당하는 특정 페이지를 표시하게 하거나 사용자가 URL을 통해 특정 페이지로 이동하는 기능을 할 수 있다.  
 - react-router: https://reactrouter.com/

<br/>

## 7.2 프로젝트 준비

```Bash
$ npx create-react-app react-router-todo --template=typescript

$ cd todo
$ npm install --save @emotion/react @emotion/styled
$ npm install --save-dev prettier eslint

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

$ npm run format:fix
$ npm run lint:fix
$ npm run format
$ npm run lint
$ npm start
```

<br/>

 - 설정 파일
```JS
// tsconfig.json
{
  "compilerOptions": {
    ..
    "jsx": "react-jsx",
    "baseUrl": "src"
  },
}

// .prettierrc.js
module.exports = {
  singleQuote: true,
  trailingComma: 'all',
  printWidth: 100,
};

// .eslintrc.js: ESLint 룰 설정
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

// package.json: ESLint, Prettier 명령어 추가
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

## 7.3 소스 코드

이전에 만든 할 일 목록 앱에서 react-router를 사용하여 페이지 이동 기능을 추가한다.  
할 일 목록 앱을 할 일 목록 페이지, 등록 페이지로 나누어볼 수 있다.  

<br/>

### react-router

 - react-router 설치
    - react-router를 사용하기 위해서는 react-router 라이브러리를 설치해야 한다.
```Bash
$ npm install react-router-dom@6 --save
```

<br/>

 - index.tsx
    - react-router를 사용하기 위해 BrowserRouter를 추가한다.
    - BrowserRouter 컴포넌트를 최상위 컴포넌트에 적용한다. react-router 기능들은 이 `<BrowserRouter />` 컴포넌트 안에서만 동작하므로 `<BrowserRouter />` 컴포넌트는 react-router 기능을 사용하는 모든 컴포넌트의 공통 부모 컴포넌트에 적용해야 한다.
```TS
const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>,
);
```

<br/>

 - App.tsx
    - URL에 따라 화면이 변경되는 부분은 react-router의 <Routes /> 컴포넌트 안에 정의해야 한다.
    - `<Routes><Route path="URL 경로" element={URL에 해당하는 컴포넌트} /></Routes>`
```TS
function App() {
  return (
    <Container>
      <ToDoListContextProvider>
        <Header />
        <Routes>
          <Route path="/" element={<DataView />} />
          <Route path="/add" element={<ToDoInput />} />
          <Route
            path="*"
            element={
              <NotFound>
                404
                <br />
                NOT FOUND
              </NotFound>
            }
          />
        </Routes>
      </ToDoListContextProvider>
    </Container>
  );
}
```

<br/>

 - DataView, ToDoInput
    - DataView와 ToDoInput 컴포넌트는 페이지를 담당하는 컴포넌트로 일반 컴포넌트들과 구별하기 위해 pages라는 폴더안에 위치시킨다.
    - react-router에서 링크가 아닌 자바스크립트로 페이지 전환을 하기 위해서는 react-router-dom이 제공하는 useNavigate 훅을 사용해야 한다.
```TS
// DataView
import styled from '@emotion/styled';
import { Title } from 'components/Title';
import { ToDoList } from 'components/ToDoList';
import { ShowInputButton } from 'components/ShowInputButton';
import { useNavigate } from 'react-router-dom';

export const DataView = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <Title label="할 일 목록" />
      <ToDoList />
      <ShowInputButton show={false} onClick={() => navigate('/add')} />
    </Container>
  );
};

// ToDoInput
export const ToDoInput = () => {
  const navigate = useNavigate();
  const { onAdd } = useContext(ToDoListContext);
  const [toDo, setToDo] = useState('');

  const onAddTodo = () => {
    if (toDo === '') return;

    onAdd(toDo);
    setToDo('');
    navigate('/');
  };

  return (
    <Container>
      <Contents>
        <Title label="할 일 추가" />
        <InputContainer>
          <TextInput value={toDo} onChange={setToDo} />
          <Button label="추가" color="#304FFE" onClick={onAddTodo} />
        </InputContainer>
      </Contents>
      <ShowInputButton show={true} onClick={() => navigate('/')} />
    </Container>
  );
};
```

<br/>

 - Header 컴포넌트
    - 일반적인 웹 사이트에서는 페이지와 상관없이 항상 표시되는 Header나 Footer, 메뉴 등을 가지고 있다.
    - useNavigate 훅을 사용하여 자바스크립트에서 클릭 이벤트가 발생했을 때 페이지를 이동할 수 있었다. Header 컴포넌트에서는 react-router가 제공하는 Link 컴포넌트를 활용하여 페이지를 이동할 수 있다.
    - URL에 따라 표시되는 페이지 컴포넌트들은 Routes 컴포넌트 하위에 Route 컴포넌트를 사용하여 표시할 수 있다. 하지만, 페이지와 상관없이 항상 표시되는 컴포넌트(Header, Footer 등)를 배치하기 위해서는 Routes 컴포넌트 외부에 표시하고자 하는 컴포넌트를 배치할 필요가 있다.
    - 즉, react-router를 사용하여 링크를 만들 때에는 a 태그가 아닌 Link 컴포넌트를 사용한다.
    - `<Link to="URL 경로">링크하고자 하는 컴포넌트 또는 문자열</Link>`
```TS
import styled from '@emotion/styled';
import { Link } from 'react-router-dom';

..

const StyledLink = styled(Link)`
  color: #ffffff;
  font-size: 20px;
  text-decoration: none;
`;

export const Header = () => {
  return (
    <Container>
      <StyledLink to="/">할 일 목록 앱</StyledLink>
    </Container>
  );
};
```

<br/>

## 7.4 요약

리액트는 UI 라이브러리로 기본적으로 페이지 이동 기능을 제공하지 않는다.  
때문에, UI와 관련되지 않은 기능을 사용하기 위해서는 외부 라이브러리를 이용하여야 한다.  
페이지 이동 기능은 react-router 라이브러리를 이용할 수 있다.  
react-router는 리액트의 생태계에서 오랜 세월 페이지 전환 기능 라이브러리로 사용되어, 리액트를 활용하여 웹 애플리케이션을 개발하는 경우 페이지 이동 라이브러리로 많이 사용된다. 
```
1. react-router 기능들은 이 <BrowserRouter /> 컴포넌트 안에서 동작하여 모든 컴포넌트의 공통 부모 컴포넌트에 존재하여야 한다.

2. URL에 따라 화면이 변경되는 부분은 react-router의 <Routes /> 컴포넌트 안에 정의해야 한다. (ex: <Routes><Route path="URL 경로" element={URL에 해당하는 컴포넌트} /></Routes>)

3. 링크가 아닌 자바스크립트로 페이지 전환을 하기 위해서는 react-router-dom이 제공하는 useNavigate 훅을 사용한다.

4. 페이지와 상관없이 항상 표시되는 컴포넌트(Header, Footer 등)에서 페이지를 이동할 때는 <Link/> 태그를 이용할 수 있다.
```