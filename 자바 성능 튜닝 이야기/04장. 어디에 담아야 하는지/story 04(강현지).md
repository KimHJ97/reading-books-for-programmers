# story 04

## Collection 인터페이스

- Collection : 가장 상위 인터페이스
- Set : 중복을 허용하지 않는 집합을 처리하기 위한 인터페이스
- SortedSet : 오름차순을 갖는 Set 인터페이스
- List : 순서가 있는 집합을 처리하기 위한 인터페이스. 중복 허용, 인덱스 있음
- Queue : 여러개의 객체를 처리하기 전에 담아서 처리할 때 사용하기 위한 인터페이스. FIFO
- Map : 키와 값의 쌍으로 구성된 객체의 집합을 처리하기 위한 인터페이스. 중복 키 허용하지 않음
- SortedMap : 키를 오름차순으로 정렬하는 Map 인터페이스

### Set 인터페이스

- HashSet : 데이터를 해쉬 테이블에 담는 클래스로 순서 없이 저장
- TreeSet : red-black이라는 트리에 데이터 저장. 값에 따라 순서가 정해짐. 데이터를 담으면서 동시에 정렬을 하기 때문에 HashSet보다 성능상 느림
- LinkedHashSet : 해쉬 테이블에 데이터를 담는데 저장된 순서에 따라 순서가 결정

**성능**

저장되는 데이터의 크기를 미리 알고있다면, 객체 생성시 미리 크기를 지정하는 것이 성능상 유리

**성능 측정**

1. 데이터 담는 경우
    1. HashSet과 LinkedHashSet의 성능이 비슷하고, TreeSet의 순서로 성능 차이 발생
2. 데이터 읽는 경우(순차적)
    1. LinkedHashSet이 가장 빠르고, HashSet, TreeSet 순으로 데이터를 가져오는 속도가 느려짐
3. 데이터 읽는 경우(비 순차적)
    1. HashSet과 LinkedHashSet의 속도는 빠르지만, TreeSet의 속도는 느림

### List 인터페이스

- Vector : 객체 생성시에 크기를 지정할 필요가 없는 배열 클래스
- ArrayList : Vector와 비슷하지만, 동기화 처리가 되어 있지 않음
- LinkedList : ArrayList와 동일하지만 Queue 인터페이스를 구현했기 때문에 FIFO 큐 작업을 수행

**성능 측정**

1. 데이터 담는 경우
    1. 어떤 클래스는 큰 차이가 없음
2. 데이터 꺼내는 경우
    1. ArrayList의 속도가 가장 빠르고, Vector와 LinkedList는 속도고 매우 느림.
    2. Vector는 여러 스레드가 접근 가능하도록 get() 메서드에 synchronized가 선언되어있어 성능이 느릴 수 밖에 없음
3. 데이터 삭제하는 경우
    1. ArrayList와 Vector는 실제로 그 안에 배열을 사용하기 때문에 첫번째 값과 마지막 값을 삭제하는 메서드의 속도 차이가 큼
    2. LinkedList는 첫번째 값과 마지막 값을 삭제하는 메서드 속도 차이가 크지 않음

### Map 인터페이스

- Hashtable : 데이터를 해쉬 테이블에 담는 클래스. 내부에서 관리하는 해쉬 테이블 객체가 동기화되어 있음
- HashMap : 데이터를 해쉬 테이블에 담는 클래스. null값 허용. 동기화되어 있지 않음
- TreeMap : red-black 트리에 데이터를 담는 클래스. 키에 의해 순서가 정해짐
- LinkedHashMap : HashMap과 거의 동일하며 이중 연결 리스트라는 방식을 사용하여 데이터를 담는다는 점만 다름

성능 측정

1. 데이터 넣는 경우
    1. 속도 비슷함
2. 데이터 꺼내는 경우
    1. 대부분의 클래스들이 동일하지만 TreeMap 클래스가 가장 느림

### Queue 인터페이스

- PriorityQueue : 큐에 추가된 순서와 상관없이 먼저 생성된 객체가 먼저 나오도록 되어있는 큐
- LinkedBlockingQueue : 저장할 데이터의 크기를 선택적으로 정할 수 도 있는 FIFO 기반의 링크 노드를 사용하는 블로킹 큐
- ArrayBlockingQueue : 저장되는 데이터의 크기가 정해져 있는 FIFO 기반의 블로킹 큐
- PriorityBlockingQueue : 저장되는 데이터의 크기가 정해져 있지 않고, 객체의 생성 순서에 따라서 순서가 저장되는 블로킹 큐
- DelayQueue : 큐가 대기하는 시간을 지정하여 처리하도록 되어 있는 큐
- SynchronousQueue : put() 메서드를 호출하면, 다른 스레드에서 take() 메서드가 호출될 때까지 대기하도록 되어 있는 큐. 이 큐에는 저장되는 데이터가 없음. API 에서 제공하는 대부분의 메서드는 0이나 null 리턴

### 각 인터페이스 별 권장 클래스

- Set : HashSet
- List : ArrayList
- Map : HashMap
- Queue : LinkedList

### Collection 관련 클래스의 동기화

JDK 1.0 버전에 생성된 Vector나 Hashtable은 동기화 처리가 되어 있지만, JDK 1.2 버전 이후에 만들어진 클래스는 모두 동기화 처리가 되어 있지 않음

Collections 클래스의 synchronized로 시작하는 메서드들은 최신 버전 클래스들의 동기화를 지원

Map의 경우 스레드에서 Iterator로 어떤 Map 객체의 데이터를 꺼내고 있는데, 다른 스레드에서 해당 Map을 수정하는 경우 ConcurrentModificationException 예외 발생 가능

⇒ java.util.concurrent 패키지의 클래스들 확인. 문제 해결을 위한 클래스들이 많음