# 네이밍

 - 클래스: 인터페이스, 열거형, 구조체, 프로토콜, 트레이트 등을 포함
 - 변수: 상수, 프로퍼티, 필드, 인수, 로컬 변수 등을 포함
 - 함수: 메서드, 프로시저, 서브루틴 등을 포함
 - 범위: 패키지, 모듈, 네임스페이스 등을 포함
 - 리소스: 파일, 디렉토리, ID 등을 포함

코드의 가독성을 높이려면 코드 네이밍은 정확하고 설명적이어야 한다.  

 - 정확: 명명된 이름과 실제로 사용되는 의미가 일치해야 한다.
 - 설명적: 이름만 보고도 그것이 무엇인지 알 수 있어야 한다.
    - w나 h라는 변수명보다 width나 height이 내용을 이해하기 쉽다.
    - 변수명이 image라면 이미지의 비트맵 데이터인지, 이미지가 존재하는 URL인지, 이미지를 표시하기 위한 뷰인지 명확하게 imageBitmap, imageUrl, imageView로 네이밍 하는 것이 더 설명적이다.

<br/>

## 1. 네이밍에 사용하는 영문법

영어 단어를 사용하여 이름을 지을 때는 영문법에 가까운 형태로 어순과 형태를 정하는 것이 좋다.  

ListenerEventMessageClickViewText 라는 변수가 있을 때 명확히 어떤 클래스인지 파악하기 힘들다.  
MessageTextViewClickEventerListener 라는 변수가 있다면, 메시지를 표시하는 텍스트 뷰에서 발생한 클릭 이벤트 리스너라고 해석할 수 있다.  
어떤 이벤트인지는 Click으로 UI의 클릭 이벤트 정보를 얻을 수 있고, 무엇에 대한 클릭 이벤트인지는 MessageTextView로 메시지 텍스트 뷰인 것을 알 수 있다.  

<br/>

### 1-1. 명사 또는 명사구

명사구를 사용할 때는 네이밍의 대상이 무엇인지를 나타내는 단어를 마지막에 두는 것이 좋다.  
 - 버튼의 높이를 표현할 때 heightButton 보다 buttonHeight이 좋다.

<br/>

다만, 범위를 한정하는 단어가 많아지면 중요한 단어를 마지막에 두는 것이 어려워진다. 예를 들어, '세로 화면 모드일 때 버튼 높이'를 네이밍을 한다면 portraitModeButtonHeight가 된다. 이럴 때는 전치사를 사욯아여 수식어를 뒤에 배치할 수 있다. 'buttonHeightInPortraitMode' 처럼 전치사 in을 사용하여 portraitMode를 뒤로 이동시킨다.  
 - 네이밍에 전치사를 사용하는 것은 변수나 함수명, 비공개 내부 클래스 등으로 제한하는 것이 좋다.
 - 여러 곳에서 사용하는 클래스명에 전치사를 사용하면 오히려 가독성을 떨어뜨릴 수 있다.

<br/>

사용자 수를 네이밍할 때 'numberOfUsers'가 된다. 가급적이면 전치사를 사용하는 것보다는 '인원수'를 의미하는 단어를 마지막에 두는 것이 좋다.  
단어의 순서를 바꾸면 usersNumber가 되는데, 식별자(ID)로 오해할 수 있다. 이때는, number를 대체할 만한 단어로 count나 total을 생각할 수 있다.  
userCount나 userTotal 이라는 명칭을 사용해 오해 소지를 줄이고, 정수 값을 나타내는 단어가 맨 마지막에 배치하여 더 명확하게 할 수 있다.  

<br/>

### 1-2. 명령문

프로시저나 메서드를 포함한 함수의 네이밍에는 명령문을 사용한다.  
명령문을 사용할 때는 동사 원형을 이름 앞에 붙이는 것이 좋다.  
만약, 명령문이 아닌 어순으로 만들거나 부사를 맨 앞에 두면 가독성이 떨어진다. 동사가 아닌, ~한 것으로 잘못 해석될 수 있다.  
 - 사용자의 동작을 기록한다.
    - 기록하다: log
    - 사용자의 동작: userAction
    - logUserAction

<br/>

### 1-3. 그 외의 영문법

 - __형용사나 형용사구 또는 분사__
    - 성질이나 상태를 나타내는 클래스나 변수에 Iterable과 같은 형용사나 Playing, Finished와 같은 분사를 사용할 수 있다.
    - 특히 단일 메서드 인터페이스나 상태를 나타내는 열거자나 상수 값에 많이 사용된다.
 - __3인칭 단수 현재형 동사 및 조동사와 그에 따른 의문문__
    - 참/거짓 값을 가지는 변수 또는 참/거짓 값을 반환하는 함수에서 사용한다.
    - contains, shouldUpdate와 같이 3인칭 단수의 현재형 동사나 조동사를 사용하거나 isTextVisible과 같이 의문문으로 네이밍한다.
 - __전치사를 수반하는 부사구__
    - toInt, fromMemberId, asSequence와 같이 타입을 변환하는 함수 또는 onFinished와 같은 콜백에서 사용한다.

<br/>

### 1-4. 문법을 무시하고 네이밍하는 이유

 - 심미성, 통일성, 일관성은 가독성을 위한 수단일 뿐 그 자체가 목적이 되면 안 된다.
 - 네이밍에 있어 가장 중요하게 생각해야 할 기준은 이름만으로도 코드를 이해할 수 있는지 여부이다.
```java
// 사용자 액션 이벤트
class UserActionEvent {};

// 이벤트 클래스의 서브 클래스
// ✔ 영문법에 따른 경우
class ClickActionEvent extends UserActionEvent {}
class DragActionEvent extends UserActionEvent {}

// ❌ 외관상 통일감에 중시하는 경우
class UserActionEventClick extends UserActionEvent {}
class UserActionEventDrag extends UserActionEvent {}

// ❌ 클릭 대상별로 나눈 이벤트 클래스
class UserActionEventClickMessageText extends UserActionEvent {}
class UserActionEventClickProfileImage extends UserActionEvent {}
```
<br/>

## 2. 이름에서 알 수 있는 내용

 - 적절한 이름: 대상이 무엇인지, 무엇을 하는지를 나타내는 이름
    - MessageListProvider: 메시지 리스트를 제공하는 클래스
    - userId: 사용자 ID
    - showErrorDialog: 오류 대화 상자를 표시하는 함수
 - 부적절한 이름: 언제, 어디서, 어떻게 사용되는지를 나타내는 이름
    - onMessageReceived: 메시지를 받았을 때 호출되는 함수
    - isCalledFromEditScreen: 편집 화면에서 호출되었을 때 true가 되는 값
    - idForNetworkQuery: 네트워크 쿼리에 사용되는 고유한 식별자

대상이 무엇인지, 무엇을 하는지를 네이밍으로 설명함으로 대상의 책임 범위가 어디까지인지, 대상을 사용하는 코드가 무엇을 수행하는지 이 두가지가 더 명확해진다.  

<br/>

### 2-1. 인수 이름

 - showUserList는 참/거짓 값을 인수로 받아 그 값에 따라 오류 대화 상자의 표시 여부를 결정한다.
 - 이때, 인수를 담을 매개변수는 t rue일 떄 무엇을 하는지 초점을 두고 네이밍해야 한다.
```java
// ✔ Good: 무엇을 하는지를 설명하는 매개변수 이름
void showUserList(boolean shouldShowDialogOnError) {
    // ..   
}

// ❌ BAD: 어디서 호출하는지를 설명하는 매개변수 이름
void showUserList(boolean isCalledFromLandingScreen) {
    // ..
}
```
<br/>

shouldShowDialogOnError로 네이밍하면 true나 false가 전달되었을 때 어떤 일이 일어나는지 함수 선언만 봐도 알 수 있다.  
하지만, isCalledFromLandingScreen로 네이밍하면 인수 값에 따라 어떤 일이 일어나는지 알려면 함수 내부의 코드를 읽어야만 한다.  

<br/>

### 2-2. 함수 이름

메시지를 받았을 때 내용을 표시하는 함수를 네이밍하면, 함수명은 '내용을 표시하다'에 초점을 맞추어 showReceivedMessage로 한다.  
반면에, 메시지를 받았을 때에 착안하여 onMessageReceived로 네이밍하는 것은 적절하지 않다.  

```java
// ✔ Good: 무엇을 하는지를 설명하는 함수 이름
class MessageViewPresenter {
    void showReceivedMessage(MessageModel model) {}
}
class MessageRepository {
    void storeReceivedMessage(MessageModel model) {}
}

presenter.showReceivedMessage(messageModel);
repository.storeReceivedMessage(messageModel);

// ❌ 언제 호출해야 하는지를 설명하는 함수 이름
class MessageViewPresenter {
    void onMessageReceived(MessageModel model) {}
}
class MessageRepository {
    void onMessageReceived(MessageModel model) {}
}

presenter.onMessageReceived(messageModel);
repository.onMessageReceived(messageModel);
```
<br/>

### 2-3. 예외: 추상 메서드

이름에는 그 대상이 무엇이며, 무엇을 할 것인가를 명시해야 한다고 설명했지만, 예외 케이스도 있다.  
예를 들어, 콜백으로 정의된 추상 메서드 등은 선언 시점에 무엇을 할 것인지가 정해져 있지 않은 경우가 많다.  
 - onClicked, onSwiped, onDestroyed, onNewMessage 등과 같이 언제, 어디서 호출되는지를 기준으로 네이밍한다.
 - 다만, 추상 메서드라도 메서드 목적이 명확하다면 무엇을 하는가를 기준으로 네이밍해야 한다.
    - 클릭되었을 때 선택 상태를 바꾼다면, 구현을 기대하는 추상 메서드는 onClicked가 아닌 toggleSelectionState로 네이밍한다.

<br/>

## 3. 단어 선택

 - 모호하지 않은 단어 선택하기
 - 혼란스러운 약어 피하기
 - 단위나 실체를 나타내는 단어 추가하기
 - 긍정적인 단어 사용하기

<br/>

### 3-1. 모호하지 않은 단어 선택하기

한계를 나타내는 limit을 사용할 때 상한선인지 하한선인지 모호하다. 그보다는 max나 min을 사용해야 더 명확하다.  

 - __모호한 단어: flag__
    - flag가 참/거짓 값으로 사용될 경우에는 true와 false의 값이 각각 무엇을 나타내는지 모호하다.
    - flag를 사용할 때는 참과 거짓이 뒤바뀔 가능성도 고려해야 한다.
```
Bad: initializationFlag
초기화 중: isInitializing
초기화 완료: wasInitialized
초기화 가능: canInitialize, isInitializable
초기화해야 함: shouldInitialize, isInitializationRequired, requiresInitialization
```
<br/>

 - __모호한 단어: check__
    - check는 무언가를 확인, 검사하다는 의미를 갖고 있지만, 함수 이름으로 사용하면  확인하고자 하는 조건이 무엇인지, 조건이 맞지 않을 때 무엇을 할 것인지, 상태를 변경하는지 등 여러 의문이 발생한다.
```
Bad: checkMessage
조건에 부합하는지 여부를 반환값 또는 예외로 알려준다: hasNewMessage, isMessageFormatValid, throwIfMessageIdEmpty
조건을 충족하는 것을 반환한다: takeSentMessages, takeMessagesIfNotEmpty
외부에서 가져온다: queryNewMessages, fetchQueuedMessageList
내부 상태를 업데이트 또는 동기화한다: updateStoredMessages, syncMessageListWithServer
외부에 통지한다: notifyMessageArrival, sendMessageReadEvent
```
<br/>

 - __모호한 단어: old__
    - old 형용사가 이름의 일부에 사용된 경우, 어떠한 상태를 old라고 하는 것인지 모호하다.
    - 비교 대상이 있는지, 어떤 조건을 충족하는지에 주목하다면 덜 모호한 단어를 선택할 수 있다.
    - 무효화된 값이더라도 외부에서 발생한 이벤트에 의해 무효화되었다면 invalidated를 사용하고, 예정된 시각에 무효화된 경우라면 expired를 사용하는 것이 좋다.
```
하나 앞의 인덱스 또는 한 단계 앞의 상태: previous
무효화된 값: invalidated, expired
변경되기 전의 값: original, unedited
이미 취득/저장된 값: fetched, cached, stored
권장되지 않는 클래스, 함수, 변수: deprecated

지정된 시각까지 메시지를 가져오는 함수
 - ❌ getOldMessages(long receviedTimeInMillis)
 - ✔ getReceivedMessagedBefore(long timeInMillis)
```
<br/>

 - __모호하지 않은 단어 찾기__
    - 의미가 더욱 분명한 단어를 찾으려면 사전이나 유의어 사전을 활용할 수 있다.
    - get, find, search, pop, calculate, fetch, query, load

<br/>

### 3-2. 혼란스러운 약어 피하기

개인이 임의로 정의한 약어는 가급적 사용하지 말아야 한다.  
애매한 의미의 약어는 코드 읽는 속도를 더디게 만든다.  
 - 약어를 사용할 때는 정의를 찾아보지 않고도 그 의미를 알 수 있을지를 고려한다.  
 - 표준화되어 사용되는 약어도 제한된 범위 내에서 사용해도 좋다.
 - 공용 클래스 이름이나 함수 이름의 경우에는 약어를 사용하지 않는 것이 좋다.

<br/>

### 3-3. 단위나 실체를 나타내는 단어 추가하기

timeout 이라는 정수형 변수가 있을 경우 단위가 밀리초인지, 초인지, 분인지 추가해주는 것이 좋다. timeoutInSecounds, timeoutInMillis  
UI의 너비나 높이 등의 길이를 표현할 때에도 네이밍에 pixels, points, inches와 같은 단어를 활용하는 것이 좋다.  
 - 단위를 타입으로 표시하는 것도 좋다.
```java
class Inch {}
class Centimeter {}

void setWidth(Inch width) {
    // ..
}
```
<br/>

### 3-4. 긍정적인 단어 사용하기

 - 긍정적인 단어 사용 지향 (isEnabled)
 - 긍정적인 단어 사용시 부정 연산자에도 가독성이 좋다. (!isEnabled)
 - 부정적인 표현을 사용해도 좋은 상황도 있다.
    - isDisabled
    - isNotEmpty
 - 부정적인 표현에 부정 연산자 사용은 좋지 않다. (이중 부정)
    - isNotDisabled -> isEnabled
    - !isNotEmpty -> isEmpty
```java
boolean isEmpty;
boolean isNotEmpty;

// ❌: 이중 부정으로 가독성 방해
if (!isNotEmpty) {}

// ✔: 부정을 반전시켜 isEmpty를 사용
if (isEmpty) {}

// ❌: 부정적인 단어와 부정어를 모두 사용하는 네이밍
boolean isNotDisabled;

// ✔: 긍정으로 반전
boolean isEnabled;
```
<br/>

## 4. 언어, 플랫폼, 코딩 규약

제일 중요한 것은 사용하는 언어나 프로젝트에서 정한 네이밍 규약이 있는 경우, 그 규약을 우선해야 한다.  
설령 납득할 수 없는 규약이더라도 개인이 임의로 판단해 그것을 어겨서는 안 된다.  

