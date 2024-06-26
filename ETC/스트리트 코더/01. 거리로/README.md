# 거리로

스트리트 코더는 업계의 인정, 명예, 충성심 외에도 이상적으로 다음과 같은 자질을 가지고 있다.  
 - 질문하기
 - 결과 중심적
 - 높은 처리량
 - 복잡성과 모호성 수용

## 최근 소프트웨어 개발의 문제점

### 너무 많은 기술

파이썬은 인터프리터 방식의 언어로 컴파일하지 않고 바로 실행된다. 또한, 선언한 변수에 대한 타입을 지정할 필요가 없어 코드를 훨씬 더 빠르게 작성할 수 있다. 이 때문에 파이썬은 C#보다 더 나은 기술인가? 꼭 그렇지는 않다. 타입 명시와 컴파일을 하지 않기 때문에 실수가 잦아진다. 즉, 테스트 혹은 프롣거션 중에만 오류를 발견할 수 있고 단순히 코드를 컴파일하는 것보다 훨씬 더 많은 비용이 들 수 있다. 대부분의 기술은 생산성 향상에 따른 트레이드오프를 가진다.  

<br/>

### 패러다임의 패러글라이딩

1980년대 프로그래밍 패러다임으로는 구조하된 프로그래밍으로 줄 번호, GOTO 문, 함수나 루프 같은 궂화된 블록에 코드를 작성한다. 이후 OOP가 등장하고 1990년대 자바와 같은 JIT 컴파일러가 사용되는 관리형 프로그래밍 언어가 등장했고, 자바스크립트를 사용한 웹 스크립팅이 나왔고, 1990년대 말에는 서서히 주류에 진입하는 함수형 프로그래밍이 등장했다.  
2000년대부터 N 계층 애플리케이션, 팻 클라이언트, 씬 클라이언트, 제네릭, MVC, MVM, MVP라는 전문 용어를 자주 사용했다. 비동기 프로그래밍은 promise, future, finally, 리액티브 프로그래밍, 그리고 마이크로서비스와 함꼐 확산되기 시작했다.  

꼭 새로운 도구와 새로운 방식이 좋지는 않다. 패턴을 올바르게 사용하는 방법과, 더 자세히 따져보는 방법, 코드 검토를 더 잘할 수 있는 방법을 알아야 한다.  

<br/>

### 기술의 블랙박스

프레임워크나 라이브러리는 일종의 패키지다. 소프트웨어 개발자는 이것을 설치하고, 설명서를 읽고 사용한다. 하지만, 대부분 패키지가 어떻게 동작하는지는 모른다.  

코드를 처음부터 읽거나 수천 페이지짜리 이론서를 뒤질필요는 없지만, 최소한 어떤 부분이 어디에, 어떻게 영향을 미치는지 정도는 알아 두어야 한다. 이를 통해 높은 수준의 프로그래밍을 위한 더 나은 결정을 내릴 수 있다.  

