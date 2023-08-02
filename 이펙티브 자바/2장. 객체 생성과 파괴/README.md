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
