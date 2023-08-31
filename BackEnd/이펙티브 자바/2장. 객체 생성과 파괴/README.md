# 2. 객체 생성과 파괴

객체를 만들어야 할 때와 만들지 말아야 할 떄는 구분하고, 올바른 객체 생성 방법과 불필요한 생성을 피하는 방법, 제때 파괴됨을 보장하고 파괴 전에 수행해야 할 정리 작업을 관리하는 요령을 알아본다.  

## 아이템 1. 생성자 대신 정적 팩토리 메서드를 고려하라.

클래스는 클라이언트에 public 생성자 대신 정적 팩토리 메서드를 제공할 수 있다.  
이 방식을 이용하면 단점과 장점 모두 존재하게 된다.

 - 장점
    - 1. 이름을 가질 수 있다.
        -  생성자에 넘기는 매개변수와 생성자 자체만으로 반환될 객체의 특성을 제대로 설명할 수 없다. 반면, 정적 팩토리는 이름만 잘 지으면 반환될 객체의 특성을 쉽게 묘사할 수 있다.
    - 2. 호출될 때마다 인스턴스를 새로 생성하지 않아도 된다.
        - 이러한 방식으로 불변 클래스는 인스턴스를 미리 만들어 놓거나 새로 생성한 인스턴스를 캐싱하여 재활용하는 식으로 불필요한 객체 생성을 피할 수 있다.
    - 3. 반환 타입의 하위 타입 객체를 반환할 수 있는 능력이 있다.
        - 하위 타입 객체를 반환할 수 있다는 것은 엄청난 유연성을 선물한다. API를 만들 때 이 유연성을 응용하면 구현 클래스를 공개하지 않고도 그 객체를 반환할 수 있어 API를 작게 유지할 수 있다.
    - 4. 입력 매개변수에 따라 매번 다른 클래스의 객체를 반환할 수 있다.
        - 반환 타입의 하위 타입이기만 하면 어떤 클래스의 객체를 반환하든 상관없다. 클라이언트는 팩토리가 건네주는 객체가 어느 클래스의 인스턴지인지 알 수도 없고 알 필요도 없다.
    - 5. 정적 팩토리 메서드를 작성하는 시점에는 반환할 객체의 클래스가 존재하지 않아도 된다.
        - 이러한 유연함은 서비스 제공자 프레임워크를 만드는 근간이 된다.  예를 들어 jdbc가 있는데, 서비스 제공자 프레임워크에서의 제공자는 서비스의 구현체이다. 이 구현체들을 클라이언트에 제공하는 역할을 프레임워크가 통제하여, 클라이언트를 구현체로부터 분리해준다.
 - 단점
    - 1. 상속을 하려면 public이나 protected 생성자가 필요하니 정적 팩토리 메서드만 제공하면 하위 클래스를 만들 수 없다.
        - 컬렉션 프레임워크의 유틸리티 구현 클래스들은 상속할 수 없다.
    - 2. 정적 팩토리 메서드는 프로그래머가 찾기 어렵다.
        - 생성자처럼 API 설명에 명확히 드러나지 않아 사용자는 정적 팩토리 메서드 방식 클래스를 인스턴스화할 방법을 알아내야 한다.
 - 정적 팩토리 메서드 명명 규칙
    - from: 매개변수를 하나 받아서 해당 타입의 인스턴스를 반환하는 형변환 메서드
        - ex) Date d = Date.from(instant);
    - of: 여러 매개변수를 받아 적합한 타입의 인스턴스를 반환하는 집계 메서드
        - ex) Set<Rank> faceCards = EnumSet.of(JACK, QUEEN, KING);
    - valueOf: from과 of의 더 자세한 버전
        - ex): BigInteger prime = BigInteger.valueOf(Integer.MAX_VALUE);
    - instance 혹은 getInstance: instance 혹은 getInstance와 같지만, 매번 새로운 인스턴스를 생성해 반환함을 보장한다.
        - ex) StackWalker luke = StackWalker.getInstance(options);
    - create 혹은 newInstance: instance 혹은 getInstance와 같지만, 매번 새로운 인스턴스를 생성해 반환함을 보장한다.
        - ex) Object newArray = Array.newInstance(classObject, arrayLen);
    - getType: getInstance와 같으나, 생성할 클래스가 아닌 다른 클래스에 팩토리 메서드를 정의할 때 사용한다. "Type"은 팩토리 메서드가 반환할 객체의 타입이다.
        - ex) FileStore fs = Files.getFileStore(path);
    - newType: newInstance와 같으나, 생성할 클래스가 아닌 다른 클래스에 팩토리 메서드를 정의할 때 사용한다. "Type"은 팩토리 메서드가 반환할 객체의 탕비이다.
        - ex) BufferedReader br = Files.newBufferedReader(path);
    - type: getType과 newType의 간결한 버전
        - List<Complaint> litany = Collections.list(legacyLitany);

<br/>

## 아이템 2. 생성자에 매개변수가 많다면 빌더를 고려하라

정적 팩토리나 생성자를 통한 인스턴스 생성에는 공통적인 문제가 하나 있다.  
그것은 생성자 매개변수가 많아질수록 생성할 때 불편함이 커진다.  

만약, 선택적 매개변수가 많은 경우에는 생성자를 점층적 생성자 패턴으로 여러 개의 생성자를 만드는 방식이 있다.  
하지만, 이 방법도 매개변수가 많아지면 인스턴스를 생성하는 코드 작성이 어려워진다.  
 - 만약, 타입이 같은 매개변수가 연달아 늘어서 있으면 찾기 어려운 버그로 이어질 수 있다.  
 - 클라이언트가 실수로 매개변수의 순서를 바꿔 건네줘도 컴파일러는 알아채지 못하고, 결국 런타임에 엉뚱한 동작을 하게 된다.
```Java
NutritionFacts cocaCola = new NutritionFacts(240, 8, 100, 0, 35, 27);
```

선택 매개변수가 많을 때 활용할 수 있는 두 번재 대안으로 자바빈즈 패턴이 있다.  
매개변수가 없는 생성자로 객체를 만든 후, 세터 메서드를 호출해 원하는 매개변수의 값을 설정하는 방식이다.  
 - 이러한 자바빈즈도 단점이 있다. 자바빈즈 패턴에서는 객체 하나를 만들려면 메서드를 여러 개 호출해야 하고, 객체가 완전히 생성되기 전까지는 일관성이 무너진 상태에 놓이게 된다.
 - 점층적 생성자 패턴에서는 매개변수들이 유효한지를 생성자에서만 확인하면 일관성을 유지할 수 있었지만, 그 장치가 완전히 사라지게 된다.
 - 일관성이 깨진 객체가 만들어지면, 버그를 심은 코드와 그 버그 때문에 런타임에 문제를 겪는 코드가 물리적으로 멀리 떨어져 있을 것으로 디버깅도 만만치 않다.
    - 이러한 단점을 완화하고자 생성이 끝난 객체를 수동으로 '얼리고(freezing)' 얼리기 전에는 사용할 수 없도록 하기도 한다.
    - 하지만, 이 방법은 다루기 어려워 실전에서 잘 사용되지 않으며, 사용하더라도 프로그래머가 freeze 메서드를 확실히 호출했는지 컴파일전에 보증할 방법이 없어서 런타임 오류에 취약하다.
```Java
NutritionFacts cocaCola = new NutritionFacts();
cocaColca.setServingSize(240);
cocaColca.setServings(8);
cocaColca.setCalories(100);
cocaColca.setSodium(35);
cocaColca.setCarbohydrate(27);
```

<br/>

세 번째 대안으로 점층적 생성자 패턴의 안전성과 자바빈즈 패턴의 가독성을 겸비한 빌더 패턴이 있다.  
클라이언트는 필요한 객체를 직접 만드는 대신, 필수 매개변수만으로 생성자를 호출해 빌더 객체를 얻는다.  
그 다음 빌더 객체가 제공하는 일종의 세터 메서드들로 원하는 선택 매개변수들을 설정한다.  
마지막으로 매개변수가 없는 build 메서드를 호출해 객체를 얻는다.  
빌더는 생성할 클래스 안에 정적 멤버 클래스로 만들어두는 게 보통이다.
 - NutritionFacts 클래스는 불변이며, 모든 매개변수의 기본값들을 한 곳에 모아둔다.
 - 빌더의 세터 메서드들은 빌더 자신을 반환하기 때문에 연쇄적으로 호출할 수 있다. 이런 방식을 메서드 호출이 흐르듯 연결된다는 뜻으로 플루언트 API 혹은 메서드 연쇄라고 한다.
    - 추가적으로 잘못된 매개변수에 대해 빌더의 생성자와 메서드에서 입력 매개변수 검사를 하고, build 메서드가 호출하는 생성자에서 여러 매개변수에 걸친 불변식을 검사한다.
    - 공격에 대비해 이런 불변식을 보장하려면 빌더로부터 매개변수를 복사한 후 해당 객체 필드들도 검사해야 한다.
    - 검사해서 잘못된 점을 발견하면 어떤 매개변수가 잘못되었는지를 메시지를 담아 IllegalArgumentException을 던지면 된다.
```Java
// 클라이언트 코드 - 필수 매개변수 지정과 선택 매개변수로 어떤 값이 들어가는지 메서드 명으로 확인할 수 있다.
NutritionFacts cocaCola = new NutritionFacts.Builder(240, 8)
            .calories(100)
            .sodium(35)
            .carbohydrate(27)
            .build();

// NutritionFacts 클래스 빌더 패턴 적용
public class NutritionFacts {

    private final int servingSize;
    private final int servings;
    ..

    public static class Builder {
        // 필수 매개변수
        private final int servingSize;
        private final int servings;

        // 선택 매개변수 - 기본값으로 초기화한다.
        private int calories = 0;
        private int fat = 0;
        ..

        public Builder(int servingSize, int servings) {
            this.servingSize = servingSize;
            this.servings = servings;
        }

        public Builder calories(int calories) {
            this.calories = calories;
            return this;
        }
        ..

        private NutritionFacts build() {
            return new NutritionFacts(this);
        }
    }

    private NutritionFacts(Builder builder) {
        this.servingSize = builder.servingSize;
        this.servings = builder.servings;
        this.calories = builder.calories;
        ..
    }
}
```

<br/>

## 아이템 3. private 생성자나 열거 타입으로 싱글턴임을 보증하라

싱글턴(Singleton)이란 인스턴스를 오직 하나만 생성할 수 있는 클래스를 말한다.  
싱글턴의 전형적인 예로는 함수와 같은 무상태 객체나 설계상 유일해야 하는 시스템 컴포넌트를 들 수 있다.  
하지만, 클래스를 싱글턴으로 만들면 이를 사용하는 클라이언트를 테스트하기가 어려워질 수 있다.  
타입을 인터페이스로 정의한 다음 그 인터페이스를 구현해서 만든 싱글턴이 아니라면 싱글턴 인스턴스를 가짜(mock) 구현으로 대체할 수 없기 때문이다.  

<br/>

싱글턴을 만드는 방법은 크게 2가지가 있다.  
2가지 방식 모두 생성자는 private으로 감춰두고, 유일한 인스턴스에 접근할 수 있는 수단으로 public static 멤버를 하나 마련한다.  

 - public static final 필드 방식의 싱글턴
    - private 생성자는 public static final 필드인 Elvis.INSTANCE를 초기화할 때 딱 한 번만 호출된다. 즉, public이나 protected 생성자가 없으므로 Elvis 클래스가 초기화될 때 만들어진 인스턴스가 전체 시스템에서 하나뿐임이 보장된다.
 - 정적 팩토리 방식의 싱글턴
    - Elvis.getInstance는 항상 같은 객체의 참조를 반환한다.
 - 싱글턴 방식별 특징
    - public 필드 방식은 해당 클래스가 싱글턴임이 명백히 들어난다. public static 필드가 final로 절대로 다른 객체를 참조할 수 없다.
    - 정적 팩토리 방식은 API를 바꾸지 않고도 싱글턴이 아니게 변경할 수 있다. 또한, 원한다면 정적 팩토리를 제네릭 싱글턴 팩토리로 만들 수 있고, 정적 팩토리의 메서드 참조를 공급자로 사용할 수도 있다.
```Java
// public static final 필드 방식의 싱글턴
public class Elvis {
    public static final Elvis INSTANCE = new Elvis();
    private Elvis() { .. }

    ..
}

// 정적 팩토리 방식의 싱글턴
public class Elvis {
    private static final Elvis INSTANCE = new Elvis();
    private Elvis() { .. }
    public static Elvis getInstance() { return INSTANCE; }

    ..
}
```

 - 원소가 하나인 열거 타입을 선언하는 방식
    - public 필드 방식과 비슷하지만, 더 간결하고, 추가 노력 없이 직렬화할 수 있고, 복잡한 직렬화 상황이나 리플렉션 공격에도 제 2의 인스턴스가 생기는 일을 완벽히 막아준다.
    - 대부분 상황에서는 원소가 하나뿐인 열거 타입이 싱글턴을 만드는 가장 좋은 방법이다.
    - 단, 만들려는 싱글턴이 Enum 외의 클래스를 상속해야 한다면 이 방법을 사용할 수 없다.
```Java
// 열거 타입 방식의 싱글턴
public enum Elvis {
    INSTANCE;

    ..
}
```

<br/>

## 아이템 4. 인스턴스화를 막으려거든 private 생성자를 사용하라

가끔 단순히 유틸리티 클래스 같은 정적 메서드와 정적 필드만을 담은 클래스를 만들고 싶은 경우가 발생한다.  
주의할 점으로는 생성자를 명시하지 않으면 컴파일러가 자동으로 기본 생성자를 만들어준다.  
즉, 정적 멤버만 담은 유틸리티 클래스에 매개변수를 받지 않는 public 생성자가 만들어지며, 사용자는 이 생성자가 자동으로 생성된 것인지 구분할 수 없다.  
실제로 공개된 API들에서도 이처럼 의도치 않게 인스턴스화할 수 있게 된 클래스가 종종 목격되곤 한다.  

<br/>

추상 클래스로 만드는 것으로는 인스턴스화를 막을 수 없다.  
인스턴스화를 막는 방법은 아주 간단한데, 컴파일러가 기본 생성자를 만드는 경우는 오직 명시된 생성자가 없을 때 뿐이다.  
때문에, private 생성자를 추가하면 클래스의 인스턴스화를 막을 수 있다.  

 - 인스턴스를 만들 수 없는 유틸리티 클래스
    - 명시적 생성자가 private으로 클래스 바깥에서는 접근할 수 없다.
    - 꼭 AssertionError를 던질 필요는 없지만, 클래스 안에서 실수로라도 생성자를 호출하지 않도록 해준다.
    - 생성자가 분명 존재하는데 호출할 수 없다. 이 상황은 직관적이지 않기 때문에 적절한 주석을 달아주는 것이 좋다.
    - 이 방식은 또한 상속을 불가능하게 하는 효과도 있다. 모든 생성자는 명시적이든 묵시적이든 상위 클래스의 생성자를 호출하게 되는데, 이를 private으로 선언하여 하위 클래스가 상위 클래스의 생성자에 접근할 길이 막혀버린다.
```Java
public class UtilityClass {
    // 기본 생성자가 만들어지는 것을 막는다.(인스턴스화 방지용)
    private UtilityClass() {
        throw new AssertionError();
    }
    ..
}
```

<br/>

## 아이템 5. 자원을 직접 명시하지 말고 의존 객체 주입을 사용하라

예를 들어, 맞춤법 검사기(SpellChecker)라는 클래스가 있다고 가정한다.  
만약, 해당 클래스를 유틸리티나 싱글턴을 이용하여 만든다고 가정한다.  
이러한 방식은 결국 단 하나의 사전만을 사용할 수 있다.  
쉽게, 언어별로 맞춤법 검사기가 제공되어야 할 때 사용할 수 없다.  
이 문제를 필드에서 final 한정자를 제거하고 다른 사전으로 교체하는 메서드를 추가할 수 있지만, 이 방식은 멀티스레드 환경에서 오류가 발생할 수 있다.  
__때문에, 사용하는 자원에 따라 동작이 달라지는 클래스에는 정적 유틸리티 클래스나 싱글턴 방식이 적합하지 않다.__

```Java
// 정적 유틸리티로 사용 - 유연하지 않고 테스트하기 어렵다.
public class SpellChecker {
    private static final Lexicon ditionary = "..";
    private SpellChecker() { .. } // 객체 생성 방지

    public static boolean is Valid(String word) { .. }
    public static List<String> suggestions(String typo) { .. }
}

// 싱글턴으로 사용 - 유연하지 않고 테스트하기 어렵다.
public class SpellChecker {
    private static final Lexicon ditionary = "..";
    private SpellChecker() { .. }
    public static SpellChecker INSTANCE = new SpellChecker(..);

    public static boolean is Valid(String word) { .. }
    public static List<String> suggestions(String typo) { .. }
}
```

<br/>

클래스가 여러 자원 인스턴스를 지원해야 하며, 클라이언트가 원하는 자원을 사용해야 하는 경우  
인스턴스를 생성할 때 생성자에 필요한 자원을 넘겨주는 의존성 주입 방식을 사용할 수 있다.  

<br/>

의존 객체 주입 패턴은 자원이 몇 개든 의존 관계가 어떻든 상관없이 잘 동작하게 된다.  
또한, 불변을 보장하여 여러 클라이언트가 의존 객체들을 안심하고 공유할 수 있다.  
의존 객체 주입은 생성자, 정적 팩토리, 빌더 모두에 똑같이 응용할 수 있다.  

<br/>

의존 객체 주입이 유연성과 테스트 용이성을 개선해주긴 하지만, 의존성이 수 천개나 되는 큰 프로젝트에서는 코드를 어지럽게 만들기도 한다.  
대거(Dagger), 주스(Guice), 스프링(Spring) 같은 의존 객체 주입 프레임워크를 사용하면 이런 어질러짐을 해소할 수 있다.


```Java
// 의존 객체 주입 패턴 사용 - 유연성과 테스트 용이성을 높여준다.
public class SpellChecker {
    private static final Lexicon ditionary;
    public  SpellChecker(Lexicon dictionary) {
        this.dictionary = Objects.requireNonNull(dictionary);
    }

    public static boolean is Valid(String word) { .. }
    public static List<String> suggestions(String typo) { .. }
}
```

<br/>

## 아이템 6. 불필요한 객체 생성을 피하라

똑같은 기능의 객체를 매번 생성하기 보다는 객체 하나를 재사용하는 편이 나을 때가 많다.  
특히 불변 객체는 언제든 재사용할 수 있다.  

```Java
// ❌ 실행될 때마다 String 인스턴스를 새로 만든다.
String s = new String("Hello");

// ✔ 새로운 인스턴스를 매번 만드는 대신 하나의 String 인스턴스를 사용한다. 
// 더 나아가 이 방식을 사용하면 같은 가상 머신 안에서 똑같은 문자열 리터럴을 사용하는 모든 코드가 같은 객체를 재사용함이 보장된다.
String s = "Hello";

// ❌ 실행될 때마다 Boolean 인스턴스를 새로 만든다.
// Java 9부터는 생성자가 deprecated로 지정되었다.
Boolean isTrue = new Boolean("true");

// ✔ 생성자 대신 정적 팩토리 메서드를 제공하는 불변 클래스에서는 정적 팩토리 메서드를 사용해 불필요한 객체 생성을 피할 수 있다.
// 생성자는 호출할 때마다 새로운 객체를 만들지만, 팩토리 메서드는 그렇지 않다.
// 불변 객체만 아니라 가변 객체라도 사용 중에 변경되지 않을 것임을 안다면 재사용할 수 있다.
Boolean isTrue = Boolean.valueOf("true");

// ❌ String.matches는 정규표현식으로 문자열 형태를 확인하는 메소드이다. 하지만, 성능이 중요한 상황에서 반복해 사용하기엔 적합하지 않다.
// 메서드 내부에서 만드는 정규표현식용 Pattern 인스턴스는, 한 번 쓰고 버려져서 곧바로 가비지 컬렉션 대상이 된다.
// Pattern은 입력받은 정규표현식에 해당하는 유한 상태 머신을 만들기 때문에 인스턴스 생성 비용이 높다.
static boolean isRomanNumeral(String s) {
    return s.matches("*(?=.)M*(C[MD]|D?C{0,3})"
        + "(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$");
}

// ✔ 정규표현식을 표현하는 (불변) Pattern 인스턴스를 클래스 초기화 과정에서 직접 생성해 캐싱해두고,
// 나중에 isRomanNumeral 메서드가 호출될 때마다 이 인스턴스를 재사용한다.
// 성능 뿐만 아니라, Pattern 인스턴스를 꺼내 이름을 지어주어 코드의 의미가 훨씬 더 잘 드러나게 된다.
public class RomanNumerals {
    private static final Pattern ROMAN = Pattern.compile(
            "*(?=.)M*(C[MD]|D?C{0,3})"
            + "(X[CL]|L?X{0,3})(I[XV]|V?I{0,3})$"
        );

    static boolean isRomanNumeral(String s) {
        return ROMAN.matcher(s).matches();
    }
}
```

<br/>

불필요한 객체를 만들어내는 또 다른 예로 오토박싱(auto boxing)을 들 수 있다.  
오토박싱은 프로그래머가 기본 타입과 박싱된 기본 타입을 섞어 쓸 때 자동으로 상호 변환해주는 기술이다.  
오토박싱은 기본 타입과 그에 대응하는 박싱된 기본 타입의 구분을 흐려주지만, 완전히 없애주는 것은 아니다.  

<br/>

"객체 생성은 비싸니 피해야 한다"로 오해하며 안 된다.  
요즘의 JVM에서는 별다른 일을 하지 않는 작은 객체를 생성하고 회수하는 일이 크게 부담되지 않는다.  
프로그램의 명확성, 간결성, 기능을 위해서 객체를 추가로 생성하는 것이라면 일반적으로 좋은 일이다.  

 - 오토박싱 성능 예제
    - sum 변수를 long이 아닌 Long으로 선언해서 불필요한 Long 인스턴스가 약 21억개나 만들어진다.
    - 단순히 sum의 타입을 long으로만 바꿔주면 6.3초에서 0.59초로 빨라질 수 있다.
    - __박싱된 기본 타입보다는 기본 타입을 사용하고, 의도치 않은 오토박싱이 숨어들지 않도록 주의한다.__
```Java
private static long sum() {
    Long sum = 0L;
    for (long i = 0; i <= Integer.MAX_VALUE; i++) {
        sum += i;
    }
    return sum;
}
```

<br/>

## 아이템 7. 다 쓴 객체 참조를 해제하라

자바 언어의 특징으로는 가비지 컬렉터를 가지고 있어, 다쓴 객체를 알아서 회수해준다.  
하지만, 이것이 절대 메모리 관리에 더 이상 신경 쓰지 않아도 된다는 것은 아니다.  

<br/>

만약, 아래와 같이 스택을 직접 구현하여 사용한다고 가정한다.  
특별한 문제가 없어보이고, 별의별 테스트를 수행해도 거뜬히 통과할 것이다.  
하지만, 여기에는 '메모리 누수' 문제가 발생할 수 있다.  
이 스택을 사용하는 프로그램을 오래 실행하다 보면 점차 가비지 컬렉션 활동과 메모리 사용량이 늘어나 결국 성능이 저하될 것이다.  
심한 경우 디스크 페이징이나 OutOfMemoryError를 일으켜 프로그램이 예기치 않게 종료되기도 한다.  

```Java
public class Stack {
    private Object[] elements;
    private int size = 0;
    private static final int DEFAULT_INITIAL_CAPACITY = 16;

    public Stack() {
        elements = new Object[DEFAULT_INITIAL_CAPACITY];
    }

    public void push(Object e) {
        ensureCapacity();
        elements[size++] = e;
    }

    public Object pop() {
        if (size == 0)
            throw new EmptyStackException();
        return elements[--size];
    }

    // 원소를 위한 공간을 적어도 하나 이상 확보한다. 배열 크기를 늘려야 할 때마다 대략 두 배씩 늘린다.
    private void ensureCapacity() {
        if (elements.length == size)
            elements = Arrays.copyOf(elements, 2 * size + 1);
    }
}
```

위에 코드에서는 스택이 커졌다가 줄어들었을 때 스택에서 꺼내진 객체들을 가비지 컬렉터가 회수하지 않는다.  
왜냐하면, 이 스택에서는 객체들의 다 쓴 참조를 계속해서 가지고 있기 때문이다.  
여기서 다 쓴 참조란 문자 그대로 앞으로 다시 쓰지 않을 참조를 뜻한다.  
앞의 코드에서는 elements 배열의 '활성 영역' 밖의 참조들이 모두 여기에 해당한다.  
활성 영역은 인덱스가 size보다 작은 원소들로 구성된다.  

<br/>

가비지 컬렉션은 의도치 않게 객체를 살려두는 메모리 누수를 찾기가 아주 까다롭다.  
객체 참조 하나를 살려두면 가비지 컬렉터는 그 객체뿐 아니라 그 객체가 참조하는 모든 객체를 회수해가지 못한다.  
그래서 단 몇개의 객체가 매우 많은 객체를 회수되지 못하게 할 수 있고 잠재적으로 성능에 악영향을 줄 수 있다.  

<br/>

해법은 간단한데, 해당 참조를 다 썼을 때 null 처리(참조 해제)하면 된다.  
예시의 스택 클래스에서는 각 원소의 참조가 더 이상 필요 없어지는 시점은 스택에서 꺼내질 때로 pop 메서드에서 꺼낸 원소를 null 처리한다.  
다 쓴 참조를 null 처리하면, null 처리한 참조를 실수로 사용하려 할 때 NullPointerException을 던지며 종료된다.  

```Java
public Object pop() {
    if (size == 0)
        throw new EmptyStackException();
    Object result = elements[--size];
    elements[size] = null; // 다 쓴 참조 해제
    return result;
}
```

<br/>

__객체 참조를 null 처리하는 일은 예외적인 경우여야 한다.__  
__다 쓴 참조를 해제하는 가장 좋은 방법은 그 참조를 담은 변수를 유효 범위(scope) 밖으로 밀어내는 것이다.__  
만약, 변수의 범위를 최소가 되게 정의했다면 이 일은 자연스럽게 이뤄진다.  
 - 자기 메모리를 직접 관리하는 클래스라면 프로그래머는 항시 메모리 누수에 주의해야 한다. 원소를 다 사용한 즉시 그 원소가 참조한 객체들을 다 null 처리해주어야 한다.
 - 메모리 누수의 주범으로는 캐시, 리스너, 콜백 등이 있을 수 있다. 이러한 경우 약한 참조로 저장하면 가비지 컬렉터가 즉시 수거해간다. (WeakHashMap에 키로 저장)

<br/>

## 아이템 8. finalizer와 cleaner 사용을 피하라

자바에서는 두 가지 객체 소멸자를 제공한다.  
그중 finalizer는 예측할 수 없고, 상황에 따라 위험하 수 있어 일반적으로 불필요하다.  
자바 9에서는 finalizer를 사용 자제(deprecated) API로 지정하고 cleaner를 그 대안으로 소개했다.  
cleaner는 finalizer보다는 덜 위험하지만, 여전히 예측할 수 없고, 느리고, 일반적으로 불필요하다.  
finalizer와 cleaner는 즉시 수행된다는 보장이 없다.  
 - finalizer와 cleaner는 안전망 역할이나 중요하지 않은 네이티브 자원 회수용으로만 사용하자. 물론 이런 경우라도 불확실성과 성능 저하에 주의해야 한다.

<br/>

## 아이템 9. try-finally보다는 try-with-resource를 사용하라

자바에서 네트워크 API, 파일 입출력 API 등 I/O 작업이 필요한 객체는 GC의 대상이 되지 않는다.  
GC의 대상은 보통 힙 메모리에 존재하는 객체를 대상으로 한다.  
쉽게, Closeable 인터페이스 상속받은 클래스들은 개발자들이 직접 닫아주어야 한다. (ex: InputStream, OutputStream, java.sql.Connection 등)  

 - try-finally
    - 
```Java
static String firstLineOfFile(String path) throws IOException {
    BufferedReader br = new BufferedReader(new FileReeader(path));
    try {
        return br.readLine();
    } finally {
        br.close();
    }
}
```

 - try-with-resource
    - JDK 7버전부터 try-with-resources 구문을 제공한다. 이 구조를 사용하기 위해서는 해당 자원이 AutoCloseable 인터페이스를 구현해야한다.
```Java
static String firstLineOfFile(String path) throws IOException {
    try (
        BufferedReader br = new BufferedReader(new FileReader(path))
    ) {
        return br.readLine();
    }
}

// 복수의 자원 처리시
static void copy(String src, String dst) throws IOException {
    try (
        InputStream in = new FileInputStream(src);
        OutputStream out = new FileOutputStream(dst);
    ) {
        byte[] buf = new byte[BUFFER_SIZE];
        int n;
        while ((n = in.read(buf)) >= 0) {
            out.write(buf, 0, n);
        }
    }
}
```