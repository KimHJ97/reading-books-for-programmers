# 다트 비동기 프로그래밍

다트 언어는 동기/비동기 프로그래밍을 지원한다.  

## 1. Future

Future 클래스는 미래라는 단어의 의미대로 미래에 받아올 값을 뜻한다.  
비동기 프로그래밍은 서버 요청과 같이 오래 걸리는 작업을 기다린 후 값을 받아와야 하기 때문에 미래값을 표현하는 Future 클래스가 필요하다.

 - Future.deplayed() 는 비동기 연산으로 코드 실행이 블로킹 되지 않고 다음 코드를 바로 실행한다.
```dart
void main() {
    addNumbers(1, 1);
}

void addNjumbers(int number1, int number2) {
    print('$number1 + $number2 계산 시작');

    // Future.delayed() 메서느는 일정 시간 후에 콜백 함수를 실행할 수 있다.
    Future.deplayed(Duration(seconds: 3), () {
        print('$number1 + $number2 = ${number1 + number2}');
    });

    print('$number1 + $number2 코드 실행 끝');
}
```
<br/>

## 2. async와 await

async와 await 키워드를 사용하면 비동기 프로그래밍을 유지하면서 코드 가독성을 유지할 수 있다.  

```dart
void main() {
    // 두 함수가 비동기로 수행된다.
    addNumbers(1, 1);
    addNumbers(2, 2);
}

// async 키워드는 함수 매개변수 정의와 바디 사이에 입력한다.
Future<void> addNumbers(int number1, int number2) async {
    print('$number1 + $number2 계산 시작');

    // await는 대기하고 싶은 비동기 함수 앞에 입력한다.
    await Future.delayed(Duration(seconds: 3), () {
        print('$number1 + $number2 = ${number1 + number2}');
    });

    print('$number1 + $number2 코드 실행 끝');
}
```
<br/>

 - `결과값 반환하기`
```dart
void main() async {
    final result = await addNumbers(1, 1);
    print('결과값: $result');

    final result2 = await addNumbers(2, 2);
    print('결과값: $result2');
}

Future<int> addNumbers(int number1, int number2) async {
    print('$number1 + $number2 계산 시작');

    // await는 대기하고 싶은 비동기 함수 앞에 입력한다.
    await Future.delayed(Duration(seconds: 3), () {
        print('$number1 + $number2 = ${number1 + number2}');
    });

    print('$number1 + $number2 코드 실행 끝');

    return number1 + number2;
}
```
<br/>

## 3. Stream

Future는 반환값을 딱 한 번 받아내는 비동기 프로그래밍에 사용한다.  
지속적으로 값을 반환 받을 때는 Stream을 사용한다. Stream은 한 번 리슨하면 Stream에 주입되는 모든 값들을 지속적으로 받아온다.  

<br/>

 - `스트림 기본 사용법`
    - 스트림을 사용하려면 플러터에서 기본으로 제공하는 'dart:async' 패키지를 불러와야 한다.
    - 그다음 'dart:async' 패키지에서 제공하는 StreamController를 listen() 해야 값을 지속적으로 반환받을 수 있다.
```dart
import 'dart:async';

void main() {
    final controller = StreamController();
    final stream = controller.stream;

    // Stream에서 listen() 함수를 실행하면 값이 주입될 떄마다 콜백 함수를 실행할 수 있다.
    final streamListener1 = stream.listen((val) {
        print(val);
    });

    // Stream에 값 주입하기
    controller.sink.add(1);
    controller.sink.add(2);
    controller.sink.add(3);
    controller.sink.add(4);
}
```
<br/>

 - `브로드캐스트 스트림`
    - 스트림은 단 한 번만 listen() 을 실행할 수 있다.
    - 하지만, 때때로 하나의 스트림을 생성하고 여러 번 listen() 함수를 실행하고 싶을 때가 있다. 이럴 때는 브로드캐스트 스트림을 사용하면 스트림을 여러 번 listen() 하도록 변환할 수 있다.
```dart
import 'dart:async';

void main() {
    final controller = StreamController();

    // 여러 번 리슨할 수 있는 Broadcast Stream 객체 생성
    final stream = controller.stream.asBroadcastStream();

    // 첫 번째 listen() 함수
    final streamListener1 = stream.listen((val) {
        print('리슨 1');
        print(val);
    });

    // 두 번째 listen() 함수
    final streamListener2 = stream.listen((val) {
        print('리슨 2');
        print(val);
    });

    // add()를 실행할 떄마다 listen() 하는 모든 콜백 함수에 값이 주입된다.
    controller.sink.add(1); // 리슨 1 수행 -> 리슨 2 수행
    controller.sink.add(2);
}
```
<br/>

 - `함수로 스트림 반환하기`
    - StreamController를 직접 사용하지 않고도 직접 스트림을 반환하는 함수를 작성할 수도 있다.
    - Future를 반환하는 함수는 async로 함수를 선언하고, return 키워드로 값을 반환하면 된다.
    - 스트림을 반환하는 함수는 async*로 함수를 선언하고, yield 키워드로 값을 반환하면 된다.
```dart
import 'dart:async';

Stream<String> calculate(int number) async* {
    for (int i = 0; i < 5; i++) {
        yield 'i = $i';
        await Future.delayed(Duration(seconds: 1));
    }
}

void playStream() {
    calculate(1).listen((val) {
        print(val);
    });
}

void main() {
    playStream();
}
```
<br/>

## 핵심 요약

 - 비동기 프로그래밍을 이용하면 오랜 기간 CPU의 리소스가 막히는 상황을 방지할 수 있다.
 - async 키워드를 사용하면 비동기 함수를 정의할 수 있다.
 - await 키워드를 사용하면 비동기 함수를 논리적 순서대로 실행할 수 있다.
 - Future는 비동기 응답을 한 번만 받을 때 사용하는 클래스이다.
 - Stream은 지속적으로 리슨하여 비동기 응답을 받을 때 사용하는 클래스이다.
    - 한 번 listen() 하면 지속적으로 값을 받아볼 수 있다.
    - async* 키워드로 정의한다.
    - 값을 반환할 때는 yield 키워드를 사용한다.
    - 함수에서 Stream을 반환할 수 있다.

