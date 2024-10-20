# 플러터 입문하기

## 1. 플러터 소개

플러터는 구글이 구현한 크로스 플랫폼 프레임워크이다.  
초기에는 안드로이드, iOS 앱만 지원했지만 현재는 웹사이트, macOS, 윈도우, 리눅스 데스크톱 앱까지 지원한다.  

<br/>

### 플러터 구조 살펴보기

플러터 프레임워크는 세 계층으로 나뉘어져 있다.  

 - 임베더 계층
    - 하드웨어와 가장 가까운 로우 레벨 계층
    - 6개 플랫폼의 네이티브 플랫폼과 직접 통신을 하고 운영체제의 자체적 기능을 모듈화해둔 계층
    - 각 플랫폼의 네이티브 언어로 작성되어 있다.
 - 엔진 계층
    - 대부분 C++로 작성되어 있으며 플러터 코어 API와 스키아 그래픽 엔진, 파일시스템 그리고 네트워크 기능 등이 정의돼 있다.
 - 프레임워크 계층
    - 플러터 프레임워크를 사용하는 데 필수적인 위젯, 애니메이션, 머티리얼 패키지, 쿠퍼티노 패키지 등이 있다.

플러터가 스키아 엔진과 직접 통신한다는 건 어떤 플랫폼이든 스키아 엔진을 지원한다면 플러터가 컴파일되고 실행되도록 구현할 수 있다는 의미이다.  
대부분 크로스 플랫폼 앱 개발 프레임워크들은 웹뷰를 사용하거나 각 플랫폼의 UI 라이브러리들을사용한다. 플러터는 웹뷰를 사용하지 않고 직접 스키아 엔진을 사용해 화면에 UI를 그려낸다. 이때 새로 렌더링이 필요한 위젯들만 렌더링하기 때문에 다른 크로스 플랫폼 앱 개발 프레임워크보다 상당히 높은 퍼포먼스를 선보인다.  

<br/>

## 2. Hello Flutter 앱 만들기

### 2-1. 안드로이드 스튜디오에서 프로젝트 생성하기

 - `GUI 환경에서 프로젝트 생성하기`
```
New Flutter Project
 - Flutter SDK path: 플러터 개발 키트 경로 지정
 - Project name: hello_world
 - Project_location: ~/StudioProjects/hello_world
 - Description: A new Flutter project.
 - Project type: Application
 - Organization: com.example
 - Android language: Kotlin
 - iOS language: Swift
 - Platforms: Android, iOS
```
<br/>

 - `CLI 환경에서 프로젝트 생성하기`
    - 안드로이드 스튜디오는 플러터 프로젝트 생성을 위한 UI 제공 뿐만 아니라, CLI로도 플러터 프로젝트를 생성할 수 있다.
```bash
flutter create hello_world2
```
<br/>

### 2-2. 가상 머신 테스트 환경

안드로이드 에뮬레이터와 iOS 시뮬레이터로 실제 기기 없이 기기를 테스트 해볼 수 있다.  

 - `안드로이드 에뮬레이터 생성하기`
```
Device Manager > Create Device
 - Select Hardware: 실행할 기기 선택
    - Phone > Pixel 2 선택 > Next
 - System Image: OS 선택
    - Tiramisu(API 33) 선택 > Next
    - 최신 버전을 사용해도 큰 문제가 되진 않지만 버전 호환으로 인한 에러가 발생할 가능성이 있다.
 - Android Virtual Device (AVD): 원하는 에뮬레이터 이름 설정
    - AVD Name: Pixel 2 API Tiramisu
    - Show Advanced Settings 클릭: 향상된 세팅 화면 출력
        - Internal Storage: 8GB    -> 앱을 설치할 충분한 용량을 설정해야 한다.

이후 Device Manager 탭을 확인하면 새로운 안드로이드 에뮬레이터가 생성되어있다.
재생 버튼을 누르면 해당 에뮬레이터를 실행할 수 있다.
```
<br/>

 - `iOS 시뮬레이터 실행하기`
    - iOS 시뮬레이터는 MacOS 환경에서만 실행할 수 있다.
    - Xcode를 정상적으로 설치 후 환경 설정이 되었다면, iOS 시뮬레이터가 자동으로 설치된다.
```

```