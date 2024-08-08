# 상태

가변 값을 불변 값으로 대체하거나, 부수 효과가 없는 함수를 사용하면 가독성과 견고함을 향상시킬 수 있다.  
하지만, 떄로는 가변 값을 사용하는 것이 더 직관적인 코드를 작성할 수도 있다.  

<br/>

## 1. 가변 값이 더 적합한 경우

```kotlin
// 가변 큐를 이용한 너비 우선 탐색 구현
fun search(valueToFind: Int, root: Node): Node? {
    val queue = ArrayDeque<Node>()
    var node: Node? = root
    while (node != null && node.value != valueToFind) {
        node.left?.let(queue::add)
        node.right?.let(queue::add)
        node = queue.poll()
    }
    return node
}

// 불변 리스트와 재귀 호출을 이용한 너비 우선 탐색 구현
fun search(valueToFind: Int, root: Node): Node? = innerSearch(valueToFind, listOf(root))

private tailrec fun innerSearch(valueToFind: Int, queue: List<Node>): Node? {
    val node = queue.firstOrNull()
    if (node == null || node.value == valueToFind) {
        return node
    }
    val nextQueue = queue.subList(1, queue.size) +
            (node.left?.let(::listOf) ?: emptyList()) +
            (node.right?(::listOf) ?: emptyList())
    return innerSearch(valueToFind, nextQueue)\
}
```
<br/>

## 2. 변수 간의 관계, 직교

두 변수가 서로 연관성이 없거나 두 변수의 값이 서로에게 영향을 주지 않는 경우, 이들 변수의 관계를 직교라고 한다.  
클래스나 모듈을 정의할 때는 변수의 관계가 직교하도록 설계하는 것이 좋다. 직교가 아닌 비직교 관계를 방치하면 잘못된 상태가 만들어지고 결국 가독성과 견고함이 떨어지게 된다.  

<br/>

### 2-1. 직교의 정의

두 변수가 있을 떄 한쪽이 취할 수 있는 값의 범위가 다른 한쪽의 값에 영향을 받지 않는, 즉 값이 독립적인 두 변수의 관계를 직교라고 한다.  
 - 비직교 관계를 배제하는 것은 코드의 가독성과 견고함을 높이기 위한 매우 중요한 기법
 - 두 변수가 가변적이고 값들이 잘못 조합될 수 있는 경우에는 값을 업데이트할 때마다 값의 조합이 유효한지 확인해야 한다.

<br/>

### 2-2. 방법: 함수로 대체하기

두 값이 종속 관계인 경우 함수로 대체할 수 있다.  
예를 들어, Status와 Text 라는 변수가 있을 때 Status에 따라 Text가 정해진다고 가정한다.  
 - 잘못된 값의 조합을 만들지 못하도록 인스턴스 생성이나 상태를 업데이트하는 인터페이스를 제한한다.
    - 생성자를 비공개로 설정하고, 팩토리 함수를 제공
    - Status 변경시 Status와 Text가 함께 변경되는 메서드 제공

<br/>

### 2-3. 방법: 한 타입으로 대체하기

두 값이 종속 관계가 아닌 경우 값을 함수로 대체하는 방법을 사용할 수 없다.  
직교 관계도, 종속 관계도 아닌 경우에는 합 타입을 사용할 수 있다. 합 타입이란 여러 타입을 묶어서 그중 하나의 값을 갖는 타입을 말한다.  

```java
// sealed class를 사용하지 않을 경우의 CoinStatusResponse
public class CoinStatusResponse {
    @Nullable private final CoinStatus coinStatus;
    @Nullable private final ErrorType errorType;

    private CoinStatusResponse(
        @Nullable CoinStatus coinStatus,
        @Nullable ErrorType errorType) {
            
        this.coinStatus = coinStatus;
        this.errorType = errorType;
    }

    // ..

    @NotNull
    public static CoinStatusResponse asResult(@NotNull CoinStatus coinStatus) {
        return new CoinStatusResponse(coinStatus, null);
    }

    @NotNull
    public static CoinStatusResponse asError(@NotNull ErrorType errorType) {
        return new CoinStatusResponse(null, errorType);
    }
}
```
<br/>

## 3. 상태 전이의 설계

### 3-1. 불변성

처음부터 상태 전이가 일어나지 않는 불변성을 가진 자료 구조를 사용하면 잘못된 상태 전이가 일어나지 않는다.  
불변성이란 정의, 대입, 객체 생성 이후에 상태가 변하지 않거나 외부에서 관찰할 수 없는 성질을 말한다.  

<br/>

### 3-2. 멱등성

객체가 취할 수 있는 상태의 수가 두 개 이하이고, 그 상태를 전환하는 함수가 한 개인 경우, 가능하면 함수가 멱등성을 지니도록 만드는 것이 좋다.  
멱등성이란 한 번 실행한 결과와 여러 번 실행한 결과가 동일하다는 개념이다.  
 - 멱등성을 지닌 함수는 그 함수를 호출하기 전에 현재 상태를 확인하지 않아도 된다.

<br/>

### 3-3. 비순환

원래 상태로 돌아가는 전이가 있다면 그 상태 전이는 순환한다고 할 수 있다.  

