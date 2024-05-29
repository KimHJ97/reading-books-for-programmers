# 다트 3.0 신규 문법

플러터 3.0 부터는 다트 3.0+ 을 사용한다.  
다트 언어의 메이저 버전이 3으로 변경되면서 추가된 문법이 생겨났다.  

<br/>

## 1. 레코드

레코드는 포지셔널 파라미터나 네임드 파라미터 중 한 가지 방식을 적용하여 사용할 수 있다.  

 - 포지셔널 파라미터를 이용한 레코드
    - 포지셔널 파라미터를 이용한 래코드는 포지셔널 파라미터로 표시한 타입 순서를 반드시 지켜야 한다.
 - 네임드 파라미터를 이용한 레코드
    - 네임드 파라미터는 포지셔널 파라미터와는 다르게 입력 순서를 지킬 필요가 없다.
    - 다만, 네임드 파라미터는 소괄호에 중괄호를 중첩하여 타입과 변수 이름을 쉼표로 구분하고 명시해주어야 한다.
```dart
void main() {
    // 포지셔널 파라미터를 이용한 레코드
    (String, int) minji = ('민지', 20); // ✅ 
    (String, int) minji2 = (20, '민지');// ❌ 래코드에 정의한 순서대로 타입을 입력하지 않으면 에러 발생

    print(minji); // (민지, 20);
    print(minji.$1); // 민지
    print(minji.$2); // 20
    
    // 네임드 파라미터를 이용한 레코드
    ({String name, int age}) gildong = (name: '길동', age: 20);
    
    print(gildong); // (name: 길동, age: 20)
}
```

<br/>

## 2. 구조 분해

구조 분해는 값을 반환받을 떄 단순히 하나의 변수로 받아오지 않고, 반환된 타입을 그대로 복제해서 타입 내부에 각각의 값을 직접 추출해오는 문법이다.  

```dart
// 🔹 리스트에서 구조 분해 사용 예제
// 직접 할당   
final newJeans = ['민지', '해린'];
final minji = newJeans[0];
final haerin = newJeans[1];

// 구조 분해 사용
final [minji, haerin] = ['민지', '해린'];

// 🔹 리스트에서의 스프레드 연산자를 이용한 구조 분해 사용 예제
final numbers = [1, 2, 3, 4, 5, 6, 7, 8];
final [x, y, ..., z] = numbers; // ✅ 중간 값들을 버릴 수 있다.

print(x); // 1
print(y); // 2
print(z); // 8

// 🔹 맵에서의 구조 분해 사용 예제
final minjMap = {'name': '민지', 'age': 19};
final {'name': name, 'age': age} = minjiMap;

print('name: $name'); // name: 민지
print('age: $age'); // age: 19

// 🔹 클래스에서의 구조 분해 사용 예제
final minji = Idol(name: '민지', age: 19);
final Idol(name: name, age: age) = minji; // 클래스 생성자 구조와 같이 구조 분해 하면 된다.

print(name);
print(age);
```
<br/>

## 3. switch문

다트 언어 3.0 버전으로 변경되면서 switch문에 스위치 표현식, 패턴 매칭, 완전 확인, 가드 절이 추가되었다.  

<br/>

### 3-1. 표현식 기능

표현식은 어떠한 값을 만들어내는 코드이다.  

```dart
String dayKor = '월요일';

// switch 문이 함수처럼 값을 반환한다.
String dayEnglish = switch (dayKor) {
    // '=>' 를 사용하면 switch 문 조건에 맞을 때 값을 반환할 수 있다.
     '월요일' => 'Monday',
    '화요일' => 'Tuesday',
    '수요일' => 'Wednesday',
    '목요일' => 'Thursday',
    '금요일' => 'Friday',
    '토요일' => 'Saturday',
    '알요일' => 'Sunday',
    // _는 default와 같은 의미로 사용된다.
    _ => 'Not Found',
};

print(dayEnglish); // Monday
```
<br/>

### 3-2. 패턴 매칭

패턴 매칭은 다트 3.0에서 추가된 기능으로 switch 문을 사용할 떄 패턴 매칭을 통해서 더욱 복잡한 조건을 형성할 수 있다.  

```dart
void switcher(dynamic anything) {
    switch (anything) {
        case 'aaa':
            print('match: aaa');
            break;
        case [1, 2]:
            // 정확히 [1, 2] 리스트만 매치
            print('match: [1, 2]');
            break;
        case [_, _, _]:
            // 3개의 값이 들어 있는 리스트 모두 매치
            print('match [_, _, _]');
            break;
        case [int a, int b]:
            // 첫 번쨰와 두 번째 값이 int인 리승트 매치
            print('match: (int $a, int $b)');
            break;
        case (String a, int b):
            // 첫 번째 값에 String, 두 번쨰 값에 int가 입력된 Record 타입 매치
            print('match: (String: $a, int: $b)');
            break;
        default:
            // 아무것도 매치 되지 않은 경우
            print('no match');
    }
}
```
<br/>

### 3-3. 엄격한 검사

엄격한 검사는 코드가 입력받을 수 있는 모든 조건을 전부 확인하고 있는지 체크하는 기술이다.  
다트 3.0+ 부터는 switch 문에서 엄격한 검사가 추가되어 모든 조건을 확인하고 있는지 컴파일 시점에 확인할 수 있다.  

```dart
void main() {
    // val에 입력될 수 있는 값은 true, false, null
    bool? val;

    // ❌ null 조건을 입력하지 않았기 떄문에 non exhaustive switch statement 에러 발생
    // null case를 추가하거나 default case를 추가해야 에러가 사라진다.
    switch (val) {
        case true:
            print('true');
        case false:
            print('false');
    };
}
```
<br/>

### 3-4. 보호 구문

switch문에는 when 키워드로 보호 구문을 추가할 수 있도록 변경되었다.  
when 키워드는 boolean으로 반환할 조건을 각 case문에 추가할 수 있으며 when 키워드 뒤에 오는 조건이 true를 반환하지 않으면 case 매치가 되지 않는다.  

```dart
void main() {
    (int a, int b) val = (1, -1);

    // val이 (int, int)로 (1, _)에 해당된다. 하지만, when 절에서 b의 값이 0보다 큰지를 검증하고 있다.
    // 때문에, default 구문이 실행된다.
    switch (val) {
        case (1, _) when val.$2 > 0:
            print('1, _');
            break;
        default:
            print('default');
    }
}
```
<br/>

## 4. 클래스 제한자

다트 3.0+ 부터 다양한 클래스 제한자가 추가되었다.  
추가된 클래스 제한자는 base, final, interface, sealed, mixin 이 있다.  
모든 클래스 제한자는 class 키워드 앞에 명시한다.  

<br/>

### 4-1. base 제한자

base 제한자는 base 클래스의 기능을 강제하는 제한자이다.  
base 키워드를 사용하게 되면 해당 클래스는 오직 상속만 할 수 있게 된다.  
base 클래스가 아닌 자식 클래스는 꼭 base, final 또는 sealed 제한자를 함꼐 사용해야 한다.  

```dart
/* a.dart */
base class Parent{}

/* b.dart */
import 'a.dart';

// ✅ 인스턴스화 가능
Parent parent = Parent();

// ✅ Child 클래스에 base 제한자 사용
base class Child extends Parent{}

// ❌ subtype of base or final is not base final or sealed 에러 발생
// base, sealed, final 제한자 중 하나가 필요
class Child2 extends Parent{}

// ❌ subtype of base or final is not base final or sealed 에러 발생
// base 클래스는 implement가 불가능
class Child3 implements Parent{}
```
<br/>

### 4-2. final 제한자

final 제한자를 사용하면 같은 파일에서 상속과 재정의를 할 수 있지만, 외부 파일에서는 할 수 없다.  
final 제한자는 base 제한자의 기능을 모두 포함한다.  

```dart
/* a.dart */
final class Parent{}

/* b.dart */
import 'a.dart';

// ✅ 인스턴스화 가능
Parent parent = Parent();

// ❌ extends 불가능
class Child extends Parent{}

// ❌ implement 불가능
class Child2 implements Parent{}
```
<br/>

### 4-3. interface 제한자

interface 제한자는 클래스를 외부 파일에서 상속받지 못하고 재정의만 할 수 있도록 제한하는 역할을 한다.  

```dart
/* a.dart */
interface class Parent{}

/* b.dart */
import 'a.dart'

// ✅ 인스턴스화 가능
Parent parent = Parent();

// ❌ extends 불가능
class Child extends Parent{}

// ✅ implement 가능
class Child2 implements Parent{}
```
<br/>

### 4-4. sealed 제한자

sealed 제한자는 sealed 클래스를 파일 외부에서 상속, 재정의 그리고 인스턴스화할 수 없도록 제한한다.  

```dart
/* a.dart */
sealed class Parent{}

/* b.dart */
import 'a.dart'

// ❌ 인스턴스화 불가능
Parent parent = Parent();

// ❌ extends 불가능
class Child extends Parent{}

// ❌ implement 불가능
class Child2 implements Parent{}
```
<br/>

### 4-5. mixin 제한자

다트 3.0부터는 mixin을 클래스에서 사용할 수 있게 되었다.  
일반 mixin과 같은 역할을 하면서 상속할 수 있다는 장점이 있다.  

```dart
mixin class MixinExample{}

// ✅ extend 가능
class Child extends MixinExample{}

// ✅ mixin으로 사용 가능
class Child2 with MixinExample{}
```
<br/>

## 핵심 요약

 - 레코드는 새로운 타입으로 네임드 파라미터와 포지셔널 파라미터가 있다.
 - 구조 분해는 탕비 내부의 각각의 값을 직접 추출해오는 문법이다.
 - switch문에는 표현식, 패턴 매칭, 완전 확인, 가드 절이 추가되어 다양한 방법으로 조건을 확인할 수 있다.
 - 객체지향 프로그래밍 언어의 특징 중 하나인 클래스의 고유성을 위해 다양한 클래스 제한자가 추가되었다.

 