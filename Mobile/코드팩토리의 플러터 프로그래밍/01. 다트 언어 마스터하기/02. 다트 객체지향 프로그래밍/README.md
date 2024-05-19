# 다트 객체지향 프로그래밍

다트 언어는 높은 완성도로 객체지향 프로그래밍을 지원한다.  
플러터 역시 객체지향 프로그래밍 중심으로 설치된 프레임워크이다.  

<br/>

## 1. 클래스

```dart
class Idol {
    // 멤버 변수
    String name = '블렉핑크';

    void sayName() {
        // 내부 속성 사용시 this 키워드 사용
        print('저는 ${this.name}입니다.');

        // 스코프 안에 같은 속성 이름이 하나만 존재하는 경우 this를 생략할 수 있다.
        print('저는 $name입니다.');
    }
}

void main() {
    // Idol 클래스 인스턴스화
    Idol blackPink = Idol();

    blackPink.sayName();
}
```
<br/>



### 생성자

생성자는 클래스의 인스턴스를 생성하는 메서드이다.  

```dart
class Idol {
    // 생성자에서 입력받는 변수들은 일반적으로 final 키워드 사용
    final String name;

    // 생성자 선언
    Idol(String name): this.name = name;

    // 생성자 선언2: 생성자의 매개변수를 변수에 저장하는 방법 생략
    // Idol(this.name)

    void sayName() {
        print('저는 ${this.name}입니다.');
    }
}

void main() {
    Idol blackPink = Idol('블랙핑크');
    blackPink.sayName();

    Idol bts = Idol('BTS');
    bts.sayName();
}
```
<br/>

 - `네임드 생성자`
    - 네임드 생성자는 네임드 파라미터와 비슷한 개념으로 일반적으로 생성하는 여러 방법을 명시하고 싶을 때 사용한다.
```dart
class Idol {
    final String name;
    final int membersCount;

    // 생성자
    Idol(String name, int membersCount)
        : this.name = name,
          this.membersCount = membersCount;
        
    // 네임드 생성자
    // {클래스명.네임드 생성자명} 형식
    Idol.fromMap(Map<String, dynamic> map)
        : this.name = map['name'],
          this.membersCount = map['membersCount'];

    // ..
}

void main() {
    // 기본 생성자
    Idol blackPink = IdolI('블랙핑크', 4);
    blackPink.sayName();

    // fromMap 네임 생성자 사용
    Idol bts = Idol.fromMap({
        'name': 'BTS',
        'membersCount': 7
    });
    bts.sayName();
}
```
<br/>

 - `프라이빗 변수`
    - 일반적으로 프라이빗 변수는 클래스 내부에서만 사용하는 변수를 뜻하지만, 다트 언어에서는 같은 파일에서만 접근 가능한 변수를 뜻한다.
```dart
class Idol {
    // 변수명이 '_'로 시작하면 프라이빗 변수로 생성된다.
    String _name;

    Idol(this._name);
}

void main() {
    Idol blackPink = Idol('블랙핑크');

    // 같은 파일에서는 _name 변수에 접근할 수 있지만,
    // 다른 파일에서는 _name 변수에 접근할 수 없다.
    print(blackPink._name);
}
```
<br/>

 - `게터/세터`
    - Getter 메서드에는 get 키워드를 사용하며 매개변수를 정의하지 않는다.
    - Setter 메서드에는 set 키워드를 사용하며 반환 타입을 지정하지 않는다.
    - 게터와 세터는 모두 변수처럼 사용하면 된다. 즉, 사용할 때 메서드명 뒤에 ()를 붙이지 않는다.
```dart
class Idol {
    String _name = '블랙핑크';

    String get name {
        return this._name;
    }

    set name(String name) {
        this._name = name;
    }
}

void main() {
    Idol blackPink = Idol();

    blackPink.name = '블랙핑크'; // 세터
    print(blackPink.name); // 게터
}
```

<br/>

## 2. 상속

상속은 어떤 클래스의 기능을 다른 클래스가 사용할 수 있게 하는 기법으로 extends 키워드를 사용해 상속할 수 있다.

 - 자식 클래스에서는 부모 클래스의 생성자를 실행해주어야 한다. 그렇지 않으면 부모 클래스의 모든 기능을 상속받더라도 변수값들이 설정되지 않아 기능이 제대로 동작하지 않을 수 있다.
```dart
class Idol {
    final String name;
    final int membersCount;

    Idol(this.name, this.membersCount);

    void sayName() {
        print('저는 ${this.name}입니다.');
    }

    void sayMembersCount() {
        print('${this.name} 멤버는 ${this.membersCount}명입니다.');
    }
}

// Idol 클래스를 상속하는 BoyGroup 클래스 정의
// BoyGroup 클래스는 Idol 크
class BoyGroup extends Idol {
    BoyGroup(
        String name,
        int membersCount
    ) : super(
        name,
        membersCount,
    );

    // 상속받지 않은 기능
    void sayMale() {
        print('저는 남자 아이돌입니다.');
    }
}

void main() {
    BoyGroup bts = BoyGroup('BTS', 7);

    bts.sayName(); // 부모 클래스 메서드
    bts.sayMembersCount(); // 부모 클래스 메서드
    bts.sayMale(); // 자식 클래스 메서드
}
```
<br/>

## 3. 오버라이드

오버라이드는 부모 클래스 또는 인터페이스에 정의된 메서드를 재정의할 때 사용된다.  
다트 언어에서는 override 키워드를 생략할 수 있다.  

```dart
class GirlGroup extends Idol {
    // super 키워드를 사용해 부모 생성자를 직접 호출해도 되고, 
    // 생성자의 매개변수로 super 키워드를 사용해도 된다.
    GirlGroup (
        super.name,
        super.membersCount
    );

    // override 키워드를 사용해 오버라이드한다.
    @override
    void sayName() {
        print('저는 여자 아이돌 ${this.name} 입니다.');
    }
}
```
<br/>

## 4. 인터페이스

상속은 공유되는 기능을 이어받는 개념이지만, 인터페이스는 공통으로 필요한 기능을 정의한 명세서 역할만을 한다.  
다트 언어에서는 인터페이스를 지정하는 키워드가 따로 없다. 상속은 단 하나의 클래스만 상속받을 수 있지만, 인터페이스는 적용 개수에 제한이 없다.  

 - 상속은 부모 클래스의 모든 기능이 상속되어 재정의할 필요가 없다.
 - 반면 인터페이스는 반드시 모든 기능을 재정의해주어야 한다.
```dart
// implements 키워드를 사용하여 원하는 클래스를 인터페이스로 사용할 수 있다.
class GirlGroup implements Idol {
    final String name;
    final int membersCount;

    GrilGroup (
        this.name,
        this.membersCount
    );

    void sayName() {
        print('저는 여자 아이돌 ${this.name} 입니다.');
    }

    void sayMembersCount() {
        print('${this.name} 멤버는 ${this.membersCount} 명입니다.');
    }
}
```
<br/>

## 5. 믹스인

믹스인은 특정 클래스에 원하는 기능들만 골라 넣을 수 있는 기능이다.  
특정 클래스를 지정해서 속성들을 정의할 수 있으며, 저장한 클래스를 상속하는 클래스에서도 사용할 수 있다.  

```dart
mixin IdolSingMixin on Idol {
    void sing() {
        print('${this.name}이 노래를 부른다.');
    }
}

// 믹스인을 적용할 떄는 with 키워드 사용
class BoyGroup extends Idol with IdolSingMixin {
    BoyGroup (
        super.name,
        super.membersCount
    );

    void sayMale() {
        print('저는 남자 아이돌입니다.');
    }
}

void main() {
    BoyGroup bts = BoyGroup('BTS', 7);

    // 믹스인에 정의된 sing() 함수 사용
    bts.sing();
}
```
<br/>

## 6. 추상

추상은 상속이나 인터페이스로 사용하는 데 필요한 속성만 정의하고 인스턴스화할 수 없도록 하는 기능이다.  

 - 추상 클래스는 추상 메서드를 선언할 수 있으며 추상 메서드는 함수의 반환 타입, 이름, 매개변수만 정의하고 함수 바디의 선언은 자식 클래스에서 필수로 정의하도록 강제한다.
 - 추상 메서드는 부모 클래스를 인스턴스화할 일이 없고, 자식 클래스들에 필수적 또는 공통적으로 정의되어야 하는 메서드가 존재할 때 사용된다.
```dart
// abstract 키워드를 사용해 추상 클래스 지정
abstract class Idol {
    final String name;
    final int membersCount;

    Idol(this.name, this.membersCount);

    void sayName();
    void sayMembersCount();
}

// 추상 클래스 구현
class GirlGroup implements Idol {
    final String name;
    final int membersCount;

    GirlGroup (
        this.name,
        this.membersCount,
    );

    void sayName() {
        print('저는 여자 아이돌 ${this.name} 입니다.');
    }

    void sayMembersCount() {
        print('${this.name} 멤버는 ${this.membersCount} 명 입니다.');
    }
}

void main() {
    GirlGroup blackPink = GirlGroup('블랙핑크', 4);

    blackPink.sayName();
    blackPink.sayMembersCount();
}
```
<br/>

## 7. 제네릭

제네릭은 클래스나 함수의 정의를 선언할 때가 아니라 인스턴스화하거나 실행할 때로 미룬다.  

```dart
// 인스턴스화할 떄 입력받을 타입을 T로 지정한다.
class Cache<T> {
    // data의 타입을 추후 입력될 T타입으로 지정한다.
    final T data;

    Cache({
        required this.data
    });
}

void main() {
    // T의 타입을 List<int> 로 지정
    final cache = Cache<List<int>> (
        data: [1,2,3],
    );

    // 제네릭에 입력된 값을 통해 data 변수 타입이 자동으로 유추된다.
    print(cache.data.reduce((value, element) => value + element));
}
```
<br/>

## 8. 스태틱

static 키워드는 인스턴스끼리 공유해야 하는 정보에 지정할 수 있다.  

```dart
class Counter {
    // static 키워드를 사용해서 static 변수 선언
    static int i = 0;

    Counter() {
        i++;
        print(i);
    }
}

void main() {
    Counter count1 = Counter(); // 1
    Counter count2 = Counter(); // 2
    Counter count3 = Counter(); // 3
}
```
<br/>

## 9. 캐스케이드 연산자

캐스케이드 연산자는 인스턴스에서 해당 인스턴스의 속성이나 멤버 함수를 연속해서 사용하는 기능이다.  

```dart
void main() {
    // cascade operator (..) 을 사용하면
    // 선언한 변수의 메서드를 연속으로 실행할 수 있다.
    Idol blackPink = Idol('블랙핑크', 4)
        ..sayName()
        ..sayMembersCount();
}
```
<br/>

## 핵심 요약

 - Class 키워드를 사용해서 클래스를 선언한다.
 - 클래스를 인스턴스화하면 클래스의 인스턴스를 변수로 저장할 수 있다.
 - 상속받으면 부모 클래스의 모든 속성을 물려받는다.
    - extrends 키워드를 사용해 상속받는다.
    - 하나의 자식 클래스는 하나의 부모 클래스만 상속받을 수 있다.
 - 오버라이드는 이미 선언되어 있는 속성을 덮어쓰는 기능이다. (재정의)
 - 인터페이스는 클래스의 필수 속성들을 정의하고 강제할 수 있는 기능이다.
    - implements 키워드를 사용해 인터페이스를 적용한다.
    - 하나의 클래스에 여러 개의 인터페이스를 적용할 수 있다.
 - 믹스인은 삳속처럼 모든 속성을 물려받지 않고 원하는 기능만 골라서 적용할 수 있다.
    - with 키워드를 사용해서 믹스인을 적용한다.
    - 하나의 클래스에 여러 개의 믹스인을 적용할 수 있다.
 - 제네릭은 변수 타입의 정의를 인스턴스화까지 미룰 수 있다.
 - 스태틱은 클래스에 직접 귀속되는 속성들이다. static 키워드를 사용해서 선언한다.
 - 캐스케이드 연산자는 인스턴스에서 해당 인스턴스의 속성이나 멤버 함수를 연속해서 호출할 때 사용한다.

