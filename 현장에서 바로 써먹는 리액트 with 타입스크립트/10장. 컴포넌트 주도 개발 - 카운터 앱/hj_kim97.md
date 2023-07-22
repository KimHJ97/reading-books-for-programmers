# 10. 컴포넌트 주도 개발 - 카운터 앱

## 10.1 카운터 앱

카운터 앱을 컴포넌트 주도 개발과 아토믹 디자인을 사용하여 개발하기 위해서는 컴포넌트를 최대한 작게 나누고, 아토믹 디자인의 원자 단위로 컴포넌트를 나누어야 한다.  
 - 원자 컴포넌트 생성 -> 유기체 컴포넌트 생성 -> 템플릿 컴포넌트 생성 -> 페이지 컴포넌트 생성
 - 원자 컴포넌트: Label, Input, Button과 같이 모든 컴포넌트들의 기초가 되며, 더 이상 작게 분해될 수 없는 컴포넌트
 - 유기체 컴포넌트: 특정 컨텍스트를 가지고 특정 영역에서만 사용되는 컴포넌트
 - 템플릿 컴포넌트: 원자, 분자 그리고 유기체를 사용하여 실제 컴포넌트를 화면에 배치하고 페이지의 구조를 잡는 데 사용되는 컴포넌트
 - 페이지 컴포넌트: 템플릿에 실제 콘텐츠를 표시하여 사용자가 볼 수 있는 최종 화면

<br/>

## 10.2 프로젝트 준비

```Bash
$ npx create-react-app cdd-counter --template=typescript

$ cd cdd-counter
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

## 10.3 소스 코드

### Title 원자 컴포넌트

 - '/src/components/atoms/Title' 디렉토리
    - index.tsx: 타이틀 컴포넌트
    - index.stories.tsx: 타이틀 스토리북 컴포넌트
        - ComponentStory, ComponentMeta: 컴포넌트의 스토리를 작성하기 위해 스토리북이 제공하는 라이브러리를 import
        - Title: 화면에 표시될 Title 컴포넌트를 불러온다.
        - export default .. ComponentMeta: 스토리북에 Title 컴포넌트의 스토리에 대한 기본 정보를 알려준다.
        - const Template: ComponentStory.. : 하나의 스토리 파일에서 여러 스토리들을 작성할 수 있도록 Title 컴포넌트의 템플릿 선언
```TS
// index.tsx
export const Title = ({ title }: Props) => {
  return <Label>{title}</Label>;
};

// index.stories.tsx
import { ComponentStory, ComponentMeta } from '@storybook/react';

import { Title } from '.';

export default {
  title: 'Atoms/Title',
  component: Title,
} as ComponentMeta<typeof Title>;

const Template: ComponentStory<typeof Title> = (args) => <Title {...args} />;

export const Default = Template.bind({});
Default.args = {
  title: 'Counter App',
};

```

<br/>

### Button 원자 컴포넌트

 - '/src/components/atoms/Button' 디렉토리
    - index.tsx: 버튼 컴포넌트
    - index.stories.tsx: 버튼 스토리북 컴포넌트
        - export default .. ComponentMeta: 스토리북에 Button 컴포넌트의 스토리에 대한 기본 정보를 알려준다.
        - const Template: ComponentStory: Button 컴포넌트의 템플릿 선언
        - export const Default.. : Button 컴포넌트 스토리북에 Props를 전달할 수 있도록 설정

```TS
// index.tsx: 버튼을 생성하는 간단한 컴포넌트로 라벨과 클릭 이벤트를 받는다.
export const Button = ({ label, onClick }: Props) => {
  return <Container onClick={onClick}>{label}</Container>;
};

// index.stories.tsx
import { ComponentStory, ComponentMeta } from '@storybook/react';

import { Button } from '.';

export default {
  title: 'Atoms/Button',
  component: Button,
} as ComponentMeta<typeof Button>;

const Template: ComponentStory<typeof Button> = (args) => <Button {...args} />;

export const Default = Template.bind({});
Default.args = {
  label: 'Button',
};
```

<br/>

### Count 원자 컴포넌트

```TS
// index.tsx: 카운터를 출력하는 간단한 컴포넌트
export const Count = ({ value }: Props) => {
  return <Container>{value}</Container>;
};

// index.stories.tsx
import { ComponentStory, ComponentMeta } from '@storybook/react';

import { Count } from '.';

export default {
  title: 'Atoms/Count',
  component: Count,
} as ComponentMeta<typeof Count>;

const Template: ComponentStory<typeof Count> = (args) => <Count {...args} />;

export const Default = Template.bind({});
Default.args = {
  value: 0,
};
```

<br/>

### Counter 유기체 컴포넌트

원자 컴포넌트를 조합하여 유기체 컴포넌트를 생성한다.  

 - '/src/components/organisms/Counter' 디렉토리
    - index.tsx: Counter 컴포넌트
    - index.stories.tsx: Counter 스토리북 컴포넌트
        - 원자 컴포넌트와 달리, 유기체 컴포넌트로 스토리북 파일 설정의 Organisms/Counter로 설정하여 원자 컴포넌트와 구별되는 새로운 그룹으로 생성한다.
```TS
// index.tsx
import { useState } from 'react';
import styled from '@emotion/styled';

import { Button } from 'components/atoms/Button';
import { Count } from 'components/atoms/Count';

const Container = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
`;

export const Counter = () => {
  const [count, setCount] = useState(0);
  return (
    <Container>
      <Button label="-" onClick={() => setCount(count - 1)} />
      <Count value={count} />
      <Button label="+" onClick={() => setCount(count + 1)} />
    </Container>
  );
};

// index.stories.tsx
import { ComponentStory, ComponentMeta } from '@storybook/react';

import { Counter } from '.';

export default {
  title: 'Organisms/Counter',
  component: Counter,
} as ComponentMeta<typeof Counter>;

const Template: ComponentStory<typeof Counter> = () => <Counter />;

export const Default = Template.bind({});
```

<br/>

### CounterApp 템플릿 컴포넌트

카운터 앱을 만들기 위한 컴포넌트들이 준비되었다.  
이제 사용자가 보게 될 화면을 구성하기 위해 아토믹 디자인의 템플릿을 만든다.  

 - '/src/components/templates/CounterApp' 디렉토리
    - index.tsx: CounterApp 컴포넌트
    - index.stories.tsx: CounterApp 스토리북 컴포넌트
        - 스토리북 파일 설정의 Templates/CounterApp로 설정하여 아토믹 디자인의 템플릿 컴포넌트 그룹으로 새롭게 만든다.
```TS
// index.tsx
import styled from '@emotion/styled';

import { Title } from 'components/atoms/Title';
import { Counter } from 'components/organisms/Counter';

const Container = styled.div`
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
`;

export const CounterApp = () => {
  return (
    <Container>
      <Title title="Counter App" />
      <Counter />
    </Container>
  );
};

// index.stories.tsx
import { ComponentStory, ComponentMeta } from '@storybook/react';

import { CounterApp } from '.';

export default {
  title: 'Templates/CounterApp',
  component: CounterApp,
} as ComponentMeta<typeof CounterApp>;

const Template: ComponentStory<typeof CounterApp> = () => <CounterApp />;

export const Default = Template.bind({});
```

<br/>

### Home 페이지 컴포넌트

템플릿 컴포넌트를 사용하여 사용자가 실제로 보게 될 컴포넌트를 제작한다.  

 - '/src/components/pages/Home' 디렉토리
    - index.tsx: Home 컴포넌트
    - index.stories.tsx: Home 스토리북 컴포넌트
        - 스토리북 파일 설정의 Pages/Home으로 설정하여 아토믹 디자인의 페이지 컴포넌트 그룹으로 새롭게 만든다.
```TS
// index.tsx
import { CounterApp } from 'components/templates/CounterApp';

export const Home = () => {
  return <CounterApp />;
};

// index.stories.tsx
import { ComponentStory, ComponentMeta } from '@storybook/react';

import { Home } from '.';

export default {
  title: 'Pages/Home',
  component: Home,
} as ComponentMeta<typeof Home>;

const Template: ComponentStory<typeof Home> = () => <Home />;

export const Default = Template.bind({});
```