# 09. 컴포넌트 주도 개발

## 9.1 컴포넌트 주도 개발

컴포넌트 주도 개발은 2017년, 소프트웨어 엔지니어인 톰 콜먼이 컴포넌트 아키텍처 및 UI 개발 프로세스의 변화를 설명하기 위해 처음 소개되었다.  
컴포넌트 주도 개발이란 사용자 인터페이스를 컴포넌트라는 작은 모듈 단위로 나눠 개발한 후 이를 조립하는 방식으로 UI를 구현하는 방법론을 말한다.  
즉, 컴포넌트라는 기본 단위의 개발을 시작으로 사용자에게 보여지는 최종적인 화면을 점진적으로 결합해 가는 방식으로 개발하는 방법론을 의미한다.  
 - 컴포넌트 주도 개발: https://www.chromatic.com/blog/component-driven-development

<br/>

큰 규모의 프론트엔드 프로젝트를 모듈식으로 세분화하여 작고 견고하며 유연한 컴포넌트를 구성함으로써 규모가 큰 프로젝트의 복잡함을 해결하고자 하는 움직임이 나타났다.  
컴포넌트 주도 개발은 복잡한 화면을 작고 견고한 컴포넌트로 분리하고, 이런 컴포넌트들을 재사용함으로써 개발 속도를 향상시키며 큰 프론트엔드 프로젝트에서도 쉽고 빠르게 개발할 수 있도록 도와준다.  
특히 리액트는 기본적인 구성을 컴포넌트로 하고 있어 컴포넌트 주도 개발을 하는 데 매우 적합하다.

<br/>

## 9.2 아토믹 디자인

아토믹 디자인은 2013년, 디자인 시스템 컨설턴트인 브래드 프로스트에 의해 처음 제안되었다. 브래드 프로스트는 화학적 관점에서 영감을 얻어 아토믹 디자인이라는 디자인 시스템을 고안해냈다.  
아토믹 디자인은 디자인 시스템을 원자, 분자, 유기체, 템플릿, 페이지 5가지 레벨로 나눠 구축하는 것을 제안한다.  
 - 아토믹 디자인: https://bradfrost.com/blog/post/atomic-web-design/

<br/>

원자는 더 이상 분해할 수 없는 가장 기본 단위가 되는 컴포넌트이다.  
예를 들어 Label, Input, Button과 같이 모든 컴포넌트들의 기초가 되며, 더 이상 작게 분해될 수 없는 컴포넌트들을 의미한다.  
또한, HTML 태그, 글꼴, 애니메이션, 컬러 팔레트 또는 레이아웃 같은 추상적인 요소도 포함될 수 있다.

<br/>

분자는 한 개 이상의 원자가 특정 목적을 위해 결합한 컴포넌트로, 하나의 단위로 함께 동작하는 컴포넌트들의 그룹이라고 할 수 있다.  
예를 들어 폼 입력에 자주 사용하는 Label과 Input 그리고 입력창 하단에 표시하는 에러 메시지 등을 하나의 컴포넌트로 묶어서 제공할 수 있는데, 이와 같은 컴포넌트를 분자로 분리할 수 있다.  

<br/>

유기체는 분자보다 좀 더 복잡하고 특정 컨텍스트를 가지고 특정 영역에서만 사용되는 컴포넌트를 의미한다.  
유기체는 사용자에게 의미 있는 정보를 전달하거나 인터랙션 할 수 있는 UI를 제공하는 특징을 가지고 있어 원자나 분자와는 다르게 재사용성이 크게 줄어드는 특징이 있다.  
예를 들어 Header, Footer, 사이드 메뉴는 유기체로써 컴포넌트로 볼 수 있다.  

<br/>

템플릿은 레이아웃과 같은 개념으로 볼 수 있다.  
원자, 분자 그리고 유기체를 사용하여 실제 컴포넌트를 화면에 배치하고 페이지의 구조를 잡는 데 사용된다.  
이는 실제 콘텐츠를 표시하기 전에 UI 요소, 레이아웃, 기능들이 어떻게 배치되고 사용되는지 정하는 와이어 프레임 또는 페이지의 스켈레톤으로 볼 수 있다.  

<br/>

페이지는 템플릿에 실제 콘텐츠를 표시하여 사용자가 볼 수 있는 최종 화면을 의미하며, 템플릿의 구체화된 인스턴스로 볼 수 있다.  
API 호출을 통해 실제 콘텐츠를 화면에 표시하고 사용자와의 인터랙션을 처리해야 하므로 사이드 이팩트가 발생할 수 밖에 없는 컴포넌트이다.  

<br/>

## 9.3 스토리북

스토리북은 컴포넌트 주도 개발을 도와주는 툴로 비즈니스 로직과 컨텍스트로부터 분리된 UI 컴포넌트를 만들 수 있으며 디자인 시스템을 구축할 수 있다.  
스토리북은 작고 고립된 컴포넌트를 빠르고 쉽게 만들 수 있게 하며, 하나의 컴포넌트에 집중하여 개발할 수 있게 해준다.  
또한, 컴포넌트 갭라을 위해 수많은 개발 환경을 실행시킬 필요 없이 스토리북만을 실행하여 개발할 수 있게 한다.  
스토리북은 리액트 뿐만 아니라 리액트 네이티브, 뷰, 앵귤러, 스벨트, 앰버 등을 지원한다.
 - 스토리북: https://storybook.js.org/

<br/>

## 9.4 프로젝트 준비

```Bash
$ npx create-react-app storybook --template=typescript

$ cd storybook
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

## 9.5 스토리북 설치 및 설정

```Bash
# 스토리북 라이브러리 설치
$ npm install --save-dev sb

# 스토리북 초기화
# 기본적으로 웹팩5 버전을 사용하지만, builder 옵션을 사용하여 성능이 더 좋은 웹팩5를 사용할 수 있다.
$ npx sb init --builder webpack5
 • Detecting project type. ✓
 • Adding Storybook support to your "Create React App" based project
  ✔ Getting the correct version of 12 packages
? We have detected that you're using ESLint. Storybook provides a plugin that gives the best experience with Storybook and helps follow best practices: https://github.com/storybookjs/eslint-plugin-storybook#readme

Would you like to install it? » (Y/n)
..
```

<br/>

## 9.6 스토리북 확인

스토리북을 설치하고 설정하면, 많은 것들이 자동으로 설치되고 설정된다.  

### .storybook 폴더

스토리북이 잘 설정됐다면, 프로젝트 루트폴더에 .storybook 폴더가 생성된다.  
해당 폴더를 열어보면, 기본적으로 main.js 파일과 preview.js 파일이 생성된다.  
.storybook/main.js 파일은 스토리북의 메인 설정 파일로 스토리북은 컴포넌트를 표시하기 위해 자체 개발 서버를 사용하는데, 이 해당 서버에 관한 설정 파일이다.  

 - main.js
    - stories: 스토리북은 보통 파일 명에 .stories. 라는 키워드를 추가하여 화면에 표시될 코드를 작성하는데, 해당 옵션을 통해 변경할 수 있다.
    - addons: 스토리북은 기본적인 긴으 외에 사용자가 특정 기능을 추가할 수 있도록 addon 기능을 제공하고 있다.
    - framework: 스토리북은 리액트 외에 다른 프레임워크도 지원한다. 어떤 프레임워크를 지원할지 지정하는 옵션이다.
```JS
import type { StorybookConfig } from '@storybook/react-webpack5';
const config: StorybookConfig = {
  stories: ['../src/**/*.mdx', '../src/**/*.stories.@(js|jsx|ts|tsx)'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/preset-create-react-app',
    '@storybook/addon-interactions',
  ],
  framework: {
    name: '@storybook/react-webpack5',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
  staticDirs: ['..\\public'],
};
export default config;
```

<br/>

 - preview.js
    - 컴포넌트를 어떻게 표시할지를 관리하는 설정 파일이다. 여기서 스토리북에서 사용하는 전역 매개 변수, 전역 코드 그리고 데코레이터를 관리할 수 있다.
    - 데코레이터는 하나의 컴포넌트가 화면에 표시될 때에 추가적으로 화면에 표시될 기능들을 제공하는 역할을 한다.
    - controls.matchers: 스토리북은 컴포넌트의 특정 Props를 변경할 수 있는 기능을 제공한다. 해당 옵션으로 특정 Props에 추가적인 기능을 표시할 수 있다. 예를 들어, 'background' 또는 'color'라는 Props가 있으면 색상 선택기를 표시하고, 'date'가 포함되어 있으면 달력을 표시하여 날짜를 변경할 수 있는 기능을 제공한다.
```JS
export const parameters = {
  actions: { argTypesRegex: '^on[A-Z].*' },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/,
    },
  },
};
```

<br/>

### .eslintrc.js 파일

 - 스토리북을 설정하면 ESLint 설정 파일에 자동으로 스퇴북 플러그인이 추가된다.
```JS
  extends: ['eslint:recommended', .. 'plugin:storybook/recommended'],
```

<br/>

### .npmrc 파일

.npmrc 파일은 npm 설정을 저장하는 파일이다.  
해당 파일을 사용하여 npm 레지스트리를 변경할 수 있다.  
기존 스토리북은 legacy-peer-deps를 사용하지 않으면 여러 문제들이 발생했다.  
 - github issue: https://github.com/storybookjs/storybook/issues/14119
```
legacy-peer-deps=true
```


<br/>

### package.json 파일

스토리북을 설정하면, package.json 파일의 "scripts"와 "eslintConfig", "devDependencies"가 자동으로 수정된다.
 - scripts: 개발을 위해 스토리북의 개발 서버를 실행하는 storybook 명령어와 개발이 완료된 스토리북을 정적 파일로 만들어 디자인 시스템으로 활용할 수 있는 build-storybook 명령어가 추가되었다.
```
{
  ..
  "scripts": {
    ..
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build"
  },
  "devDependencies": {
    "@storybook/addon-essentials": "^7.0.27",
    "@storybook/addon-interactions": "^7.0.27",
    "@storybook/addon-links": "^7.0.27",
    "@storybook/blocks": "^7.0.27",
    "@storybook/preset-create-react-app": "^7.0.27",
    "@storybook/react": "^7.0.27",
    "@storybook/react-webpack5": "^7.0.27",
    "@storybook/testing-library": "^0.0.14-next.2",
    "babel-plugin-named-exports-order": "^0.0.2",
    "eslint": "^8.45.0",
    "eslint-plugin-storybook": "^0.6.12",
    "prettier": "^3.0.0",
    "prop-types": "^15.8.1",
    "sb": "^7.0.27",
    "storybook": "^7.0.27",
    "webpack": "^5.88.1"
  }
}
```

<br/>

### ./src/stories 폴더

스토리북을 설정하면 ./src/stories 폴더에 스토리북이 제공하는 샘플 코드가 자동으로 생성된다.  
스토리북은 리액트 컴포넌트들을 Buttons.stories.tsx, Header.stories.tsx, Page.stories.tsx 파일들을 통해 스토리북 화면에 표시되도록 한다. 이런 각각의 스토리북용 파일을 스토리북에서는 스토리라고 부른다.  

<br/>

## 9.7 스토리북 실행

```Bash
$ npm run storybook

# http://localhost:6006/ 접속
```