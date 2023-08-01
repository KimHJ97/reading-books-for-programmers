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


