# 11. CDD - 할 일 목록 앱

## 11.1 할 일 목록 앱

 - 할 일 목록
    - 원자 컴포넌트
        - AppTitle
        - PageTitle
        - Label
        - Button
        - Input
    - 유기체 컴포넌트
        - ToDoItem: 사용자에게 할 일이라는 정보를 전달하고, 사용자의 인터렉션에 의해 해당 할 일이 삭제된다.
        - Header: 사용자에게 특정 정보를 전달한다.
        - InputToDo: 할 일이라는 데이터를 저장하는 긴으을 가진다.
    - 템플릿 컴포넌트
        - ToDoList: 할 일 목록 템플릿
        - ToDoInput: 할 일 추가 템플릿
    - 페이지 컴포넌트
        - ToDoListPage: 할 일 목록 페이지
        - ToDoInputPage: 할 일 추가 페이지
        - NotFound

<br/>

## 11.2 프로젝트 준비

```Bash
$ npx create-react-app cdd-todo --template=typescript

$ cd cdd-todo
$ npm install --save @emotion/react @emotion/styled
$ npm install --save-dev prettier eslint sb

$ npx eslint --init
..

$ npm run format:fix
$ npm run lint:fix
$ npm run format
$ npm run lint

$ npx sb init --builder webpack5
..
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

## 11.3  소스 코드

### 원자 컴포넌트

원자 컴포넌트는 atoms 디렉토리 하위에 관리하고, 스토리북에 ATOMS 메뉴 그룹으로 보이도록 한다.  

#### AppTitle 원자 컴포넌트

단순히 "할 일 목록 앱" 이라는 문자열을 화면에 출력하는 컴포넌트
 - 타이틀을 누르면 홈 화면("/")으로 이동하도록 react-router-dom의 Link 컴포넌트를 이용한다. 하지만, 이러한 페이지 이동 기능은 BrowserRouter 컴포넌트 하위에 존재하지 않으면 에러가 발생한다.

```TS
// index.tsx
import styled from '@emotion/styled';
import { Link } from 'react-router-dom';

const Container = styled(Link)`
  color: #ffffff;
  font-size: 20px;
  text-decoration: none;
  cursor: pointer;
`;

export const AppTitle = () => {
  return <Container to="/">할 일 목록 앱</Container>;
};

// index.stories.tsx
import { ComponentStory, ComponentMeta } from '@storybook/react';

import { AppTitle } from '.';

export default {
  title: 'Atoms/AppTitle',
  component: AppTitle,
  parameters: {
    backgrounds: {
      default: 'Header background color',
      values: [{ name: 'Header background color', value: '#304ffe' }],
    },
  },
} as ComponentMeta<typeof AppTitle>;

const Template: ComponentStory<typeof AppTitle> = () => <AppTitle />;

export const Default = Template.bind({});
```

<br/>

#### PageTitle 원자 컴포넌트

단순히 Props로 전달받은 문자열을 화면에 출력하는 컴포넌트

```TS
// index.tsx
export const PageTitle = ({ title }: Props) => {
  return <Container>{title}</Container>;
};

// index.stories.tsx
export default {
  title: 'Atoms/PageTitle',
  component: PageTitle,
} as ComponentMeta<typeof PageTitle>;

const Template: ComponentStory<typeof PageTitle> = (args) => <PageTitle {...args} />;

export const Default = Template.bind({});
Default.args = {
  title: '할 일 목록',
};
```

<br/>

#### Label 원자 컴포넌트

단순히 Props로 전달받은 문자열을 화면에 출력하는 컴포넌트

```TS
// index.tsx
export const Label = ({ label }: Props) => {
  return <Container>{label}</Container>;
};

// index.stories.tsx
export default {
  title: 'Atoms/Label',
  component: Label,
} as ComponentMeta<typeof Label>;

const Template: ComponentStory<typeof Label> = (args) => <Label {...args} />;

export const Default = Template.bind({});
Default.args = {
  label: '리액트 공부하기',
};
```

<br/>

#### Button 원자 컴포넌트

단순히 Props로 전달받은 문자열로 Button 태그를 만들어 화면에 출력하고, Props로 전달받은 클릭 이벤트를 수행한다.

```TS
// index.tsx
export const Button = ({ label, color = '#ff5722', onClick }: Props) => {
  return (
    <Container color={color} onClick={onClick}>
      {label}
    </Container>
  );
};

// index.stories.tsx
export default {
  title: 'Atoms/Button',
  component: Button,
} as ComponentMeta<typeof Button>;

const Template: ComponentStory<typeof Button> = (args) => <Button {...args} />;

export const RedButton = Template.bind({});
RedButton.args = {
  label: '삭제',
};

export const BlueButton = Template.bind({});
BlueButton.args = {
  label: '추가',
  color: '#304FFE',
};
```

<br/>

#### Input 원자 컴포넌트

단순히 화면에 Input 태그를 출력한다. 값과 변경 이벤트를 Props로 전달받는다.

```TS
// index.tsx
export const Input = ({ value, onChange }: Props) => {
  return <TextInput value={value} onChange={(event) => onChange(event.target.value)} />;
};

// index.stories.tsx
export default {
  title: 'Atoms/Input',
  component: Input,
} as ComponentMeta<typeof Input>;

const Template: ComponentStory<typeof Input> = (args) => <Input {...args} />;

export const Default = Template.bind({});
Default.args = {
  value: '리액트 공부하기',
};
```

<br/>

### 유기체 컴포넌트

원자 컴포넌트를 조합하여 유기체 컴포넌트를 만든다.  
유기체 컴포넌트는 organisms 디렉토리 하위에 관리하고, 스토리북에 ORGANISMS 메뉴 그룹으로 보이도록 한다.  

#### Header 유기체 컴포넌트

원자 컴포넌트인 AppTitle 컴포너트를 가져와 화면에 표시하도록 구성한다.

```TS
// index.tsx
export const Header = () => {
  return (
    <Container>
      <AppTitle />
    </Container>
  );
};

// index.stories.tsx
export default {
  title: 'Organisms/Header',
  component: Header,
} as ComponentMeta<typeof Header>;

const Template: ComponentStory<typeof Header> = () => <Header />;

export const Default = Template.bind({});
```

<br/>

#### ToDoItem 유기체 컴포넌트

할 일 목록 페이지의 유기체 컴포넌트인 ToDoItem 컴포넌트를 제작한다.  
Label, Button 원자 컴포넌트를 사용하여 유기체 컴포넌트를 만든다.  

```TS
// index.tsx
export const ToDoItem = ({ label, onDelete }: Props) => {
  return (
    <Container>
      <Label label={label} />
      <Button label="삭제" onClick={onDelete} />
    </Container>
  );
};

// index.stories.tsx
export default {
  title: 'Organisms/ToDoItem',
  component: ToDoItem,
} as ComponentMeta<typeof ToDoItem>;

const Template: ComponentStory<typeof ToDoItem> = (args) => <ToDoItem {...args} />;

export const Default = Template.bind({});
Default.args = {
  label: '리액트 공부하기',
};
```

<br/>

#### InputToDo 유기체 컴포넌트

할 일 목록 앱의 할 일 추가 페이지에 필요한 유기체 컴포넌트를 제작한다.  
사용자의 입력 데이터를 저장할 수 있도록 State를 추가한다.  
Context API를 이용하여 할 일 목록 상태를 관리할 수 있도록 한다.  
또한, 추가 버튼을 클릭하여 Context에 할 일이 추가되고, useNagivate 훅으로 할 일 목록 페이지("/")로 이동하도록 한다.

```TS
// index.tsx
export const InputToDo = () => {
  const [toDo, setToDo] = useState('');
  const { onAdd } = useContext(ToDoListContext);
  const navigate = useNavigate();

  const onAddTodo = () => {
    if (toDo === '') return;

    onAdd(toDo);
    setToDo('');
    navigate('/');
  };

  return (
    <Container>
      <Input value={toDo} onChange={setToDo} />
      <Button label="추가" color="#304FFE" onClick={onAddTodo} />
    </Container>
  );
};

// index.stories.tsx
export default {
  title: 'Organisms/InputToDo',
  component: InputToDo,
} as ComponentMeta<typeof InputToDo>;

const Template: ComponentStory<typeof InputToDo> = () => <InputToDo />;

export const Default = Template.bind({});
```

<br/>

 - contexts/ToDoList
```TS
import { createContext, useState } from 'react';

interface Context {
  readonly toDoList: string[];
  readonly onAdd: (toDo: string) => void;
  readonly onDelete: (toDo: string) => void;
}

const ToDoListContext = createContext<Context>({
  toDoList: [],
  /* eslint-disable @typescript-eslint/no-empty-function */
  onAdd: (): void => {},
  onDelete: (): void => {},
  /* eslint-enable @typescript-eslint/no-empty-function */
});

interface Props {
  children: JSX.Element | JSX.Element[];
}

const ToDoListContextProvider = ({ children }: Props) => {
  const [toDoList, setToDoList] = useState(['리액트 공부하기', '운동하기', '책 읽기']);

  const onDelete = (todo: string) => {
    setToDoList(toDoList.filter((item) => item !== todo));
  };

  const onAdd = (toDo: string) => {
    setToDoList([...toDoList, toDo]);
  };

  // console.log(toDoList);

  return (
    <ToDoListContext.Provider
      value={{
        toDoList,
        onAdd,
        onDelete,
      }}
    >
      {children}
    </ToDoListContext.Provider>
  );
};

export { ToDoListContext, ToDoListContextProvider };
```

<br />

### 템플릿 컴포넌트

<br/>

#### ToDoList 템플릿 컴포넌트

PageTitle 원자 컴포넌트로 타이틀을 구성하고,  
ToDoItem 유기체 컴포넌트를 반복하여 할 일 목록을 구성한다.  
Button 원자 컴포넌트로 할 일 추가 버튼을 구성한다.  
useNavigate 훅을 이용하여 할 일 추가 버튼이 클릭되었을 때 할 일 추가 페이지("/add")로 요청되도록 한다.

```TS
// index.tsx
export const ToDoList = ({ toDoList, onDelete }: Props) => {
  const navigate = useNavigate();

  return (
    <Container>
      <Contents>
        <PageTitle title="할 일 목록" />
        <ToDoListContainer>
          {toDoList.map((toDo) => (
            <ToDoItem
              key={toDo}
              label={toDo}
              onDelete={() => {
                if (typeof onDelete === 'function') onDelete(toDo);
              }}
            />
          ))}
        </ToDoListContainer>
      </Contents>
      <ButtonContainer>
        <Button label="할 일 추가" color="#304FFE" onClick={() => navigate('/add')} />
      </ButtonContainer>
    </Container>
  );
};

// index.stories.tsx
export default {
  title: 'Templates/ToDoList',
  component: ToDoList,
} as ComponentMeta<typeof ToDoList>;

const Template: ComponentStory<typeof ToDoList> = (args) => <ToDoList {...args} />;

export const Default = Template.bind({});
Default.args = {
  toDoList: [],
};

export const WithToDoList = Template.bind({});
WithToDoList.args = {
  toDoList: ['리액트 공부하기', 'CDD 공부하기', '할 일 목록 앱 개발하기'],
};
```

<br/>

#### ToDoInput 템플릿 컴포넌트

PageTitle 원자 컴포넌트로 타이틀을 구성하고,  
InputToDo 유기체 컴포넌트로 할 일 추가 Input을 구성한다.  

```TS
// index.tsx
export const ToDoInput = () => {
  const navigate = useNavigate();

  return (
    <Container>
      <Contents>
        <PageTitle title="할 일 추가" />
        <InputToDo />
      </Contents>
      <ButtonContainer>
        <Button label="닫기" onClick={() => navigate('/')} />
      </ButtonContainer>
    </Container>
  );
};

// index.stories.tsx
export default {
  title: 'Templates/ToDoInput',
  component: ToDoInput,
} as ComponentMeta<typeof ToDoInput>;

const Template: ComponentStory<typeof ToDoInput> = () => <ToDoInput />;

export const Default = Template.bind({});
```

<br/>

### 페이지 컴포넌트

<br/>

#### ToDoListPage 페이지 컴포넌트

할 일 목록 앱의 각 페이지에 해당하는 페이지 컴포넌트를 템플릿 컴포넌트를 활용하여 만든다.  
할 일 목록 상태는 Context API를 이용하여 받아오고, 해당 상태를 템플릿 컴포넌트에 넘긴다.  

```TS
// index.tsx
export const ToDoListPage = () => {
  const { toDoList, onDelete } = useContext(ToDoListContext);

  return <ToDoList toDoList={toDoList} onDelete={onDelete} />;
};

// index.stories.tsx
export default {
  title: 'Pages/ToDoListPage',
  component: ToDoListPage,
} as ComponentMeta<typeof ToDoListPage>;

const Template: ComponentStory<typeof ToDoListPage> = () => (
  <ToDoListContextProvider>
    <ToDoListPage />
  </ToDoListContextProvider>
);

export const Default = Template.bind({});
```

<br/>

#### ToDoInputPage 페이지 컴포넌트

단순히 ToDoInput 템플릿 컴포넌트를 페이지로 불러온다.

```TS
// index.tsx
export const ToDoInputPage = () => {
  return <ToDoInput />;
};

// index.stories.tsx
export default {
  title: 'Pages/ToDoInputPage',
  component: ToDoInputPage,
} as ComponentMeta<typeof ToDoInputPage>;

const Template: ComponentStory<typeof ToDoInputPage> = () => <ToDoInputPage />;

export const Default = Template.bind({});
```

<br/>

#### NotFound 페이지 컴포넌트

할 일 목록 페이지와 할 일 추가 페이지 이외에 URL로 이동한 경우 페이지가 존재하지 않음을 알려주기 위한 404 페이지이다.  
단순히 문자열을 출력하는 페이지로 원자 컴포넌트를 만들 필요 없이 바로 페이지 컴포넌트를 작성한다.  

```TS
// index.tsx
export const NotFound = () => {
  return (
    <Container>
      404
      <br />
      NOT FOUND
    </Container>
  );
};

// index.stories.tsx
export default {
  title: 'Pages/NotFound',
  component: NotFound,
} as ComponentMeta<typeof NotFound>;

const Template: ComponentStory<typeof NotFound> = () => <NotFound />;

export const Default = Template.bind({});
```

<br/>

### App.tsx

만든 페이지 컴포넌트들과 react-router-dom을 사용하여 할 일 목록 앱을 개발한다.  

```TS
import { BrowserRouter, Routes, Route } from 'react-router-dom';

import { ToDoListContextProvider } from 'contexts/ToDoList';

import { Header } from 'components/organisms/Header';
import { ToDoListPage } from 'pages/ToDoListPage';
import { ToDoInputPage } from 'pages/ToDoInputPage';
import { NotFound } from 'pages/NotFound';

function App() {
  return (
    <ToDoListContextProvider>
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<ToDoListPage />} />
          <Route path="/add" element={<ToDoInputPage />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </ToDoListContextProvider>
  );
}

export default App;
```