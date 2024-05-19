# 다트 입문하기

## 1. 다트 소개

다트 프로그래밍 언어는 구글이 개발하여 2011년 10월 GOTO 컨퍼런스에서 공개되었습니다.  
구글은 크롬에 Dart 가상 머신을 심어 자바스크립트를 대체하려는 시도를 했지만, 웹 개발에 혼란을 가져온다는 여론으로 결국 다트 언어를 자바스크립트로 완전 컴파일 가능하게 만드는 데 그쳤습니다.  

 - 다트 언어는 UI를 제작하는 데 최적화되어 있습니다. 완전한 비동기 언어이며 이벤트 기반입니다. 또한 아이솔레이트를 이용한 동시성 기능도 제공합니다.
 - NULL Safety, Spread Operator, Collection IF 등 효율적으로 UI를 코딩할 수 있는 기능을 제공합니다.
 - 효율적인 개발 환경을 제공해줍니다. 핫 리로딩을 통해 코드의 변경 사항을 즉시 화면에 반영할 수 있습니다.
 - 멀티 플랫폼에서 로깅하고, 디버깅하고, 실행할 수 있습니다.
 - AOT 컴파일이 가능하기 때문에 어떤 플랫폼에서든 빠른 속도를 자랑합니다.
 - 자바스크립트로의 완전한 컴파일을 지원합니다.
 - 백엔드 프로그래밍을 지원합니다.

<br/>

다트 네이티브 플랫폼은 JIT 컴파일 방식과 AOT 컴파일 방식을 사용합니다.  
JIT 컴파일 방식은 다트 가상 머신에서 제공하는 기능으로 코드의 변경 사항을 처음부터 다시 컴파일할 필요 없이 즉시 화면에 반영 할 수 있는 핫 리로딩 기능, 실시간으로 메트릭스를 확인할 수 있는 기능, 디버깅 기능을 제공합니다.  
개발 시에는 하드웨어 리소스를 적게 사용하는 것보다는 빠르게 개발하기 위한 효율을 위해 JIT 컴파일 방식을 사용하지만, 배포 시에는 리소스를 효율적으로 사용하기 위해 AOT 컴파일 방식을 사용합니다. AOT 컴파일 방식을 사용하면 ARM64나 x64 기계어로 다트 언어가 직접 컴파일 되어 매유 효율적으로 프로그램을 실행할 수 있습니다.  

<br/>

## 2. 다트 기초 문법

 - 다트 패드: https://dartpad.dev

다트는 프로그램 시작점인 엔트리 함수 기호로 main()을 사용합니다.  
주석 기호로는 //와 /**/ 그리고 /// 를 사용합니다.  
print() 함수는 문자열을 콘솔에 출력합니다.  

```dart
void main() {
    // 한 줄 주석

    /*
     * 여러 줄 주석
     * 여러 줄 주석2
     */
    
    /// 슬래시 세 개는 문서 주석을 작성할 수 있습니다.
    /// DartDoc이나 안드로이드 스튜디오 같은 IDE에서 문서로 인식합니다.

    print('Hello World!');
}
```
<br/>

### 2-1. 변수 선언

__var__ 키워드는 변수에 값이 들어가면 자동으로 타입을 추론합니다. 한 번 유추하면 추론된 타입이 고정됩니다.  
__dynamic__ 키워드는 변수의 타입이 고정되지 않습니다.  
__final과 const__ 키워드는 변수의 값을 처음 선언 후 변경할 수 없습니다. final은 런타임, const는 빌드타임 상수입니다. 즉, DateTime.now() 처럼 런타임의 시간으로 초기화할 떄 final 키워드를 사용하면 정상적으로 동작하고, const 키워드를 사용하면 에러가 발생하게 됩니다. 코드를 실행하지 않은 상태에서 값이 확정되면 const, 실행될 떄 확정되면 final을 사용합니다.  

모든 변수는 고유의 변수 타입을 갖고 있습니다. var 키워드로 자동으로 변수 타입 추론이 가능하지만, 직접적으로 변수 타입을 명시함으로써 코드를 더욱 직관적으로 작성할 수 있습니다.  

```dart
void main() {
    // var 키워드: 유추된 타입 고정
    var varVariable = "문자열 타입";
    varVariable = "문자열만 입력 가능";

    // dynamic 키워드: 동적으로 타입 변경 가능
    dynamic dynamicVariable = "동적 타입";
    dynamicVariable = 123;

    // 상수
    final DateTime now = DateTime.now(); // 런타임 상수
    const PI = 3.14; // 컴파일 상수

    // 변수 타입
    String name = "홍길동";
    int isInt = 10;
    double isDouble = 2.5;
    bool isTrue = true;
}
```
<br/>

### 2-2. 컬렉션

컬렉션은 여러 값을 하나의 변수에 저장할 수 있는 타입입니다.  
여러 값을 순서대로 저장하거나(List), 특정 키값을 기반으로 빠르게 값을 검색해야 하거나(Map), 중복된 데이터를 제거할 떄 사용됩니다(Set). 컬렉션 타입은 서로의 타입을 자유롭게 형변환이 가능하다는 장점이 있습니다.  

<br/>

#### List 타입

리스트(List) 타입은 여러 값을 순서대로 한 변수에 저장할 때 사용됩니다.  
리스트 타입에는 기본으로 제공하는 함수가 많이 있으며, add(), where(), map(), reduce()가 많이 사용됩니다.  
 - add(): 값을 추가
 - where(): 리스트를 순회하며, 조건에 맞는 값만 필터링
 - map(): 리스트를 순회하며, 값을 가공
 - reduce(): 리스트를 순회하며, 값을 누적합니다. 반환값은 List 입니다.
 - fold(): reduce()와 실행 논리는 같지만, 반환 타입을 변경할 수 있다.

```dart
void main() {
    List<String> blackPinkList = ['리사', '지수', '제니', '로제'];
    
    print(blackPinkList);
    print(blackPinkList[0]); // 첫 원소: 리사
    print(blackPinkList[3]); // 마지막 원소: 로제
    print(blackPinkList.length); // 길이 반환: 4

    // add(): 값을 추가
    blackPinkList.add('홍길동');
    
    // where(): 리스트 순회 + 조건에 맞는 값만 필터링
    final newList = blackPinkList.where(
        (name) => name == '리사' || name == '지수'
    );
    print(newList); // (리사, 지수) : Iterable 타입
    print(newList.toList()); // [리사, 지수]: Iterable -> List

    // map(): 리스트 순회 + 값 가공
    final newBlackPink = blackPinkList
                .map((name) => '블랙핑크 $name')
                .toList();
    print(newBlackPink); // 블랙핑크 리사, 블랙핑크 지수, ..

    // reduce(): 리스트 순회 + 이전 값 누적
    final allMembers = blackPinkList
                        .reduce((value, element) => 
                            value + ', ' + element
                        );
    print(allMembers); // 리사, 지수, 제니, ..

    // fold(): 리스트 순회 + 이전 값 누적 -> 반환 타입 지정 가능
    final allMembers2 = blackPinkList
                        .fold<int>(0, (value, element) =>
                            value + element.length
                        );
    print(allMembers2); // 11
}
```
<br/>

#### Map 타입

맵(Map) 타입은 키와 값의 쌍을 저장합니다. 키를 이용해서 원하는 값을 빠르게 찾는 데 중점을 둡니다.  

```dart
void main() {
    Map<String, String> dictionary = {
        'Harry Potter': '해리 포터',
        'Ron Weasley': '론 위즐리',
        'Hermione Granger': '헤르미온느 그레인저',
    };
    print(dictionary['Harry Potter']); // 해리 포터
    print(dictionary.keys); // 키 목록 반환: Harry Potter, Ron Weasley, ..
    print(dictionary.values); // 값 목록 반환: 해리 포터, 론 위즐리, ..
}
```
<br/>

#### Set 타입

세트(Set)는 중복 없는 값들의 집합입니다.  

```dart
void main() {
    Set<String> blackPink = {'로제', '로제', '지수', '리사', '제니'};
    print(blackPink); // 로제, 지수, 리사, 제니
    print(blackPink.contains('로제')); // 값이 있는지 확인
    print(blackPink.toList()); // 리스트로 변환

    List<String> blackPinkList = ['로제', '지수', '리사', '제니'];
    print(Set.from(blackPinkList)); // List -> Set 타입으로 변환
}
```
<br/>

#### enum

enum은 한 변수의 값을 몇 가지 옵션으로 제한하는 기능입니다. 선택지가 제한적일 때 사용합니다.  

```dart
enum Status {
    approved,
    pending,
    rejected,
}

void main() {
    Status status = status.approved;
}
```
<br/>

### 2-3. 연산자

연산자는 수치 연산자, null 관련 연산자, 값 비교 연산자, 타입 비교 연산자, 논리 연산자 등이 있습니다.  
 - dart 언어에서는 null 값을 가질 수 있는지 지정해주어야 null 값이 저장될 수 있습니다.

```dart
void main {
    // 기본 수치 연산자
    double number = 2;
    print(number + 2); // 4
    print(number - 2); // 0
    print(number * 2); // 4
    print(number / 2); // 1
    print(number % 3); // 2

    // null 관련 연산자
    double? number1 = 1; // 타입 뒤에 ? 키워드로 null 지정이 가능
    double? number; // null
    number ??= 3; // ??를 사용하면 값이 null일 떄 해당 값이 저장된다.
    
    // 값 비교 연산자
    int num1 = 1;
    int num2 = 2;
    print(num1 > num2); // 1 > 2: false
    print(num1 >= num2); // 1 >= 2: false
    print(num1 < num2); // 1 < 2: true
    print(num1 <= num2); // 1 <= 2: true
    print(num1 == num2); // 1 == 2: false
    print(num1 != num2); // 1 != 2: true

    // 타입 비교 연산자 (is, is!)
    String name = '홍길동';
    
    print(name is int); // false
    print(name is String); // true
    print(name is! int); // true
    print(name is! String); // false

    // 논리 연산자 (&&, ||)
    bool? result;
    result = true && true; // 모두 true면 true
    result = true && false; // 하나라도 false면 false
    result = true || false; // 하나라도 true면 true
    result = false || false; // 모두 false면 false
}
```
<br/>

### 2-4. 제어문

제어문으로는 if문, switch문, for문, while문이 있습니다.  

```dart
enum Status {
    APPROVED,
    PENDING,
    REJECTED,
}

void main() {
    // if 문
    int number = 2;

    if (number % 3 == 0) {
        print('3의 배수');
    } else if (number % 3 == 1) {
        print('나머지가 1인 경우')
    } else {
        print('맞는 조건이 없음')
    }

    // switch 문
    Status status = Status.APPROVED;

    switch (status) {
        case Status.APPROVED:
            print('승인 상태입니다.');
            break;
        case Status.PENDING:
            print('대기 상태입니다.');
            break;
        case Status.REJECTED:
            print('거절 상태입니다.');
            break;
        default:
            print('상태를 알 수 없습니다.');
    }

    // for 문
    for (int i = 0; i < 10; i++) {
        print(i); // 0 ~ 9 까지 출력
    }

    // for in
    List<int> nums = [1, 2, 3, 4, 5];
    for (int num in nums) {
        print(num); // 1, 2, 3, ..
    }

    // while 문
    int total = 0;
    while (total < 10) {
        total += 1;
    }
    print(total); // 10

    // do-while 문
    total = 0;
    do {
        total += 1;
    } while(total < 10);
    print(total); // 10
}
```
<br/>

### 2-5. 함수와 람다

함수를 사용하면 여러 곳에서 재활용할 수 있습니다. 반환할 값이 없을 떄는 void 키워드를 사용합니다.  
다트 언어는 이름이 있는 매개변수 방식인 네임드 파라미터 함수를 제공합니다. 이때, required 키워드로 필수 매개변수를 지정할 수도 있습니다. required 키워드를 정의하면, null 값이 불가능한 타입이면 기본값을 지정해주거나, 필수로 입력해야 합니다.  

```dart
// 기본 함수 (포지셔널 파라미터, 고정된 매개변수, 위치 매개변수)
int add(int a, [int b = 2]) {
    return a + b;
}

// 네임드 파라미터 함수
int addNamed({
    required int a,
    int b = 2 // 기본 값 지정
}) {
    return a + b;
}

// 포지셔널 파라미터와 네임드 파라미터 함께 사용
int addThreeNumbers (
    int a, {
    required int b,
    int c = 4,
}) {
    return a + b + c;
}

void main() {
    int? result;
    result = add(1, 2);
    result = addNamed(a: 1, b: 2);
    result = addThreeNumbers(1, b: 3, c: 7);
}
```
<br/>

#### 익명 함수와 람다 함수

익명 함수와 람다 함수는 둘 다 함수 이름이 없습니다. 이 둘은 함수 이름이 없고, 일회성으로 사용된다는 공통점이 있습니다. 통상적으로 많은 언어에서 익명 함수와 람다 함수를 구분하지만 다트에서는 구분하지 않습니다.  

``` dart
// 익명 합수
(매개변수) {
    함수 바디
}

// 람다 함수
(매개 변수) => 단  하나의 스테이트먼트
```
<br/>

 - `예제 코드`
```dart
void main() {
    List<int> numbers = [1, 2, 3, 4, 5];

    // 익명 함수
    final total = numbers.reduce((value, element) {
        return value + element;
    });
    print(total); // 15

    // 람다 함수
    final total2 = numbers.reduce((value, element) =>
        value + element
    );
    print(total2); // 15
}
```
<br/>

#### typedef와 함수

typeof 키워드는 함수의 시그니처를 정의하는 값으로 볼 수 있습니다.  
시그니처는 반환값 타입, 매개변수 갯수와 타입 등을 말합니다. 즉, 함수 선언부를 정의하는 키워드입니다.  

다트에서는 함수는 일급 객체로 함수를 값처럼 사용할 수 있습니다. 즉, typedef로 선언한 함수를 매개변수로 넣어 사용할 수도 있습닌다.  

```dart
typedef Operation = void Function(int x, int y);
```
<br/>

 - `예제 코드`
```dart
typedef Operation = int Function(int x, int y);

int add(int x, int y) {
    return x + y;
}

int subtract(int x, int y) {
    return x - y;
}

void main() {
    Operation oper = add;
    oper(1, 2); // 3

    oper = subtract;
    oper(1, 2); // -1
}
```
<br/>

 - `활용 예시`
```dart
typedef Operation = void Function(int x, int y);

void add(int x, int y) {
    print('합계: ${x+y}');
}

void calculate(int x, int y, Operation oper) {
    oper(x, y);
}

void main() {
    calculate(1, 2, add);
}
```
<br/>

### 2-6. try catch

try catch 문은 특정 코드의 실행을 시도(try) 해보고 문제가 있다면 에러를 잡는(catch) 키워드 입니다.  

```dart
void main() {
    try {
        // 시도할 로직
        print("처리중 ..");

        throw Exception('예외 발생!!!');
    } catch (e) {
        // 에러가 발생한 경우 처리할 로직
        print(e);
    }
}
```
<br/>

## 3. 핵심 요약

 - JIT 컴파일은 변경된 코드만 컴파일 하는 방식입니다. 핫 리로드 기능은 변경된 내용을 UI에 뿌려줍니다. 컴파일 시간을 단축시켜주므로 개발할 떄 유용합니다.
 - AOT 컴파일은 시스템에 최적화해 컴파일하는 방식으로 런타임 성능을 개선핳고, 저장 공간을 절약하고, 설치와 업데이트 시간을 단축시켜 배포할 떄 적합한 방식입니다.
 - 다트 언어가 자동으로 타입을 유추하는 변수를 선언할 떄는 var 키워드를 사용합니다.
 - Dart의 기본 타입에는 String, int, double, bool 이 있습니다.
 - dynamic 키워드는 어떤 타입이든 저장할 수 있는 변수를 선언할 때 사용합니다.
 - 다트 언어의 대표적인 컬렉션 타입은 List, Map, Set 입니다.
    - List는 여러 값을 순서대로 저장하는 컬렉션
    - Map은 키와 값을 짝을 지어 저장하는 컬렉션
    - Set은 중복되는 값이 존재하지 않는 컬렉션
 - typedef는 함수의 시그니처만 정의할 수 있습니다.
