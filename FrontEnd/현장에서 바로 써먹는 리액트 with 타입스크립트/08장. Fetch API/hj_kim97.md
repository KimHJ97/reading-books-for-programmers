# 08. Fetch API

## 8.1 Fetch API

자바스크립트에서 사용자의 동작 또는 페이지를 표시한 후 서버에 데이터를 요청하거나 데이터를 저장하는 데 Ajax를 사용하게 된다.  
이전에는 XMLHttpRequest를 사용하여 서버에 있는 데이터를 저장하거나 불러왔지만, 최근에는 Fetch API를 사용하여 서버에 있는 데이터를 가져오거나 저장할 수 있다.  
 - Fetch API: https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch
 - JSONPlaceholder: https://jsonplaceholder.typicode.com/
    - JSONPlaceholder는 무료로 테스트용 데이터를 제공한다. 실제로 새로운 데이터를 저장하거나 불러올 수는 없다. 새로운 데이터를 저장하는 URL은 존재하지만, 실제로 데이터가 저장되지는 않는다.
```JS
fetch(URL, {
    method: 'POST', // 사용할 메소드 (GET, POST, PUT, DELETE)
    headers: { 'content-Type': 'application/json' }, // 요청 Header에 전달할 값
    body: JSON.stringfy(data), // 요청 Body에 전달할 값
    mode: 'cors', // cors, no-cors, same-origin 등
    credentials: 'include', // 자격 증명을 위한 옵션(include, same-origin, omit)
    cache: 'no-cache', // 캐시 사용 여부(no-cache, reload, force-cache, only-if-cached)
})
```

<br/>

## 8.2 프로젝트 준비

```Bash
$ npx create-react-app blog --template=typescript

$ cd blog
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

## 8.3 소스 코드

 - GET /posts: https://jsonplaceholder.typicode.com/posts
    - 블로그 글의 제목과 본문의 일부분을 리스트 형식으로 표시하도록 한다.

<br/>

 - useEffect
    - useEffect 훅의 첫 번째 매개 변수에는 콜백 함수를 설정할 수 있으며, 이 콜백 함수는 useEffect 훅의 역할을 정의한다.
    - useEffect 훅의 두 번째 매개 변수에는 배열을 전달하는데, 빈 배열을 전달하게 되면, 클래스 컴포넌트의 componentDidMount 라이프사이클 함수와 같은 역할을 수행하게 된다. (컴포넌트가 처음 화면에 표시된 후 useEffect 훅이 한 번만 호출된다.)
    - 두 번째 매개 변수를 생략하면, 클래스 컴포넌트의 componentDidMount와 componentDidUpdate의 역할을 동시에 하게 된다. (컴포넌트 처음 렌더링 후 실행되고, Props나 State 변경에 의해 리렌더링 후에도 계속 실행)
    - 첫 번째 콜백 함수가 반환하는 함수는 componentWillUnmount 라이프사이클 함수와 같은 역할을 한다. (라이브러리와의 연동 해제 및 타이머 해제 등에 사용된다.)
    - useEffect 훅은 함수 컴포넌트에서 클래스 컴포넌트의 라이프사이클 함수와 비슷한 역할도 하지만, useEffect 훅만의 고유한 기능도 제공한다. 두 번째 매개 변수 배열에 특정 변수를 설정하여 전달하면, 모든 Props와 State 변경에 호출되는 componentDidUpdate와 달리 전달된 변수가 변경될 때에만 이 함수가 호출되도록 설정할 수 있다.
    - useEffect 훅은 클래스 컴포넌트의 라이프사이클 함수와 다르게 한 컴포넌트안에서 여러 번 정의하여 사용할 수 있다.
```TS
// 빈 배열: componentDidMount
useEffect(() => {
  ..
}, []);

// 생략: componentDidMount, componentDidUpdate
useEffect(() => {
  ..
});

// 함수 반환: componentWillUnmount
useEffect(() => {
  ..
  Return () => {

  };
});

// 특정 변수: componentDidUpdate 특정 값에만 동작
useEffect(() => {
  ..
}, [posts]);
```

<br/>

 - Header 컴포넌트
```TS
export const Header = () => {
  return (
    <Container>
      <Title>블로그 포스트</Title>
    </Container>
  );
};
```

<br/>

 - BlogPost 컴포넌트
    - 블로그 목록 API는 여러 블로그 글을 리스트 형식으로 제공한다. 따라서 하나의 블로그 글 컴포넌트를 만든 후 반복문을 사용하면, 블로그 글 목록 화면을 구성할 수 있다.
```TS
export const BlogPost = ({ title, body }: Props) => {
  return (
    <Container>
      <Title>{title}</Title>
      <Body>{body}</Body>
    </Container>
  );
};
```

<br/>

 - App 컴포넌트
    - 블로그 글 목록을 출력한다.
    - 블로그 글 정보 타입(interface)을 정의하고, useState로 블로그 글 목록 상태를 정의한다. 이때, 초깃값으로 빈 리스트를 가지도록 설정한다. 이렇게 생성한 블로그 글 목록 상태(State) 변수를 사용하여 화면에 글 목록을 반복하여 BlogPost 컴포넌트로 보여준다.
    - 블로그 글 목록 상태의 초기값은 useEffect 훅을 사용할 수 있다. useEffect 훅은 클래스형 컴포넌트의 componentDidMount 라이프사이클 함수와 같은 역할을 수행한다. 즉, 처음 렌더링 후 1회만 실행되는 함수로 외부 API 수행 후 초깃값을 정의하는데 유용하게 사용된다.

```TS
interface Post {
  readonly id: number;
  readonly userId: number;
  readonly title: string;
  readonly body: string;
}

function App() {
  const [posts, setPosts] = useState<ReadonlyArray<Post>>([]);
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/posts')
      .then((response) => response.json())
      .then((json) => setPosts(json))
      .catch((error) => {
        console.error(error);
      });
  }, []);

  return (
    <Container>
      <Header />
      {posts.map((post) => (
        <BlogPost key={post.id} title={post.title} body={post.body} />
      ))}
      <ButtonContainer>
        <Button label="등록" onClick={() => setShowForm(true)} />
      </ButtonContainer>
      {showForm && <Form onClose={() => setShowForm(false)} />}
    </Container>
  );
}
```

<br/>

 - Button 컴포넌트
    - 자주 사용되는 버튼을 컴포넌트로 만든다. 버튼의 이름(label)과 클릭 이벤트(onClick 함수)를 Props로 받는다.
```TS
interface Props {
  readonly label: string;
  readonly color?: string;
  readonly onClick?: () => void;
}

export const Button = ({ label, color = '#ff5722', onClick }: Props) => {
  return (
    <Container color={color} onClick={onClick}>
      {label}
    </Container>
  );
};
```

<br/>

 - Form 컴포넌트
    - 블로그 글을 등록할 수 있는 컴포넌트
    - 내부의 상태(State)로 제목(title)과 내용(body)를 관리한다. 사용자 입력에 따라 onChange에서 상태가 변경될 수 있도록한다. 글 등록시 State의 변수인 title과 body에 데이터가 있는 경우 JSONPlaceholder가 제공하는 API를 사용하여 데이터를 전송한다.
```TS
export const Form = ({ onClose }: Props) => {
  const [title, setTitle] = useState('');
  const [body, setBody] = useState('');

  const registerPost = () => {
    if (title === '' || body === '') return;

    fetch('https://jsonplaceholder.typicode.com/posts', {
      method: 'POST',
      body: JSON.stringify({
        userId: 1,
        title,
        body,
      }),
      headers: {
        'Content-type': 'application/json; charset=UTF-8',
      },
    })
      .then((response) => response.json())
      .then((json) => {
        console.log(json);
        if (typeof onClose === 'function') onClose();
      })
      .catch((error) => {
        console.error(error);
      });
  };

  return (
    <Container>
      <Background />
      <Contents>
        <Title>블로그 글 등록</Title>
        <InputGroup>
          <Label>Title: </Label>
          <Input value={title} onChange={(e) => setTitle(e.target.value)} />
        </InputGroup>
        <InputGroup>
          <Label>Body: </Label>
          <Input value={body} onChange={(e) => setBody(e.target.value)} />
        </InputGroup>
        <Actions>
          <Button label="등록하기" onClick={registerPost} />
          <Button label="닫기" color="#304FFE" onClick={onClose} />
        </Actions>
      </Contents>
    </Container>
  );
};
```