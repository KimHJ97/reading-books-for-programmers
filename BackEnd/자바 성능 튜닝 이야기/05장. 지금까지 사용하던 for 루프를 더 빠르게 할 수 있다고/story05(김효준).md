# 05. 지금까지 사용하던 for 루프를 더 빠르게 할 수 있다고?

* 1. 조건문(if, switch)
* 2. 반복문(for, 개선된 for)

## 1. 조건문

### 1-1. if문

```
순차적으로 if 조건문을 확인하기 떄문에 일반적으로 if문에서 분기를 많이 하면 시간이 많이 소요된다고 생각한다.
```

* 테스트

Random 클래스를 이용하여 랜덤한 값을 생성하고, if문을 테스트한다.  
10, 100, 1000개의 if문이 존재하는 테스트를 진행한다. (loop 1000번씩)  
if문 10개: 0.46 (ms)  
if문 100개: 5 (ms)  
if문 1000개: 63 (ms)  

* 결론

모든 테스트는 1000번씩 반복을 한 테스트로  
if가 하나만 있을 경우에는 기존 코드 대비 약 "응답시간/1,000"만큼 소요된다고 볼 수 있다. (nano seconds 단위)  
즉, 아주 큰 성능 저하가 발생한다고 보기 어렵다.  

__결과적으로 if문 조건이 아무리 많더라도 단순 연산이나 대소 비교의 경우 성능에 이슈가 없다.__  

### 1-2. switch 문

```
switch문은 JDK 6까지 byte, short, char, int 4가지 타입을 사용한 조건 분기만 가능했다.  
하지만, JDK 7부터는 String도 가능하다.  
```

* switch 문 방식

switch 문의 case 레이블에 해당하는 값이 정수 형식이어야 했기 때문입니다.  
따라서 String 뿐 만 아니라, float, double과 같은 다른 데이터 타입은 switch 문의 case에 직접 사용할 수 없었습니다.  

* JDK 7부터 String 비교가 어떻게 가능할까?

JDK 7부터 switch 문의 String 비교가 가능한 이유는 Object 클래스에 선언되어 있는 hashCode() 메소드 덕분입니다.  
즉, switch 문으로 작성한 코드에 String 비교를 하게 되면,  
String 클래스에서 재정의한 hashCode() 메소드로 int 값으로 사용된다.  

* hashCode()가 뭔데?

hashCode() 메소드는 Object 클래스의 메소드로, 객체의 해시 코드 값을 반환하는 역할을 합니다.  
즉, hashCode() 메소드는 객체를 구분하기 위한 정수값을 생성하는데 사용됩니다.  

hashCode() 메소드는 기본적으로 객체의 메모리 주소를 이용하여 해시 코드 값을 생성합니다.  
하지만, 때로는 객체의 내부 상태를 고려하여 해시 코드 값을 생성해야 할 떄가 있습니다.  
이 경우에는 hashCode() 메소드를 재정의하여 내부 상태를 기반으로 고유한 해시 값을 생성합니다.  
객체의 필드 값을 조합하여 해시 코드를 계산하는 방식을 사용할 수 있습니다.  
  
추가적으로 equals() 메소드는 두 객체의 내부 상태를 비교하여 동등성을 판단합니다.  
※ hashCode() 메소드와 equals() 메소드는 서로 다른 기능을 수행하지만, 객체의 동등성 판단에 있어 둘 사이에 일관성이 필요합니다.  
※ equals() 메소드로 두 객체를 비교하여 true를 반환하면, 두 객체의 hashCode() 값은 반드시 동일해야 합니다.  
※ equals()를 오버라이딩 할 때에는 반드시 hashCode()도 동일한 결과를 내도록 함께 오버라이딩 해주어야 한다. (항상 함꼐 오버라이딩)  


* 테스트

소스 코드
```Java
	public static void main(String[] args) {
		String message = "";
		switch(message) {
		case "a":
			System.out.println("a");
			break;
		case "b":
			System.out.println("b");
			break;
		case "가":
			System.out.println("가");
			break;
		case "나":
			System.out.println("나");
			break;
		default:
			System.out.println("c");
		}
	}
```

컴파일 후 디컴파일 코드
```Java
	public static void main(String[] args) {
		String message = "";
		String str1;
		switch ((str1 = message).hashCode()) {
			case 97:
				if (str1.equals("a"))
				break;
			case 98:
				if (str1.equals("b"));
				break;
			case 44032:
				if (str1.equals("가"));
				break;
			case 45208:
				if (!str1.equals("나"));
				break
			..
  }
```

* 결론

단순히 영문자의 경우 아스키 코드 번호로 컴파일 시점에 변경되었고,  
한글같은 문자의 경우는 해당 문자열(String)의 hashCode() 한 값으로 변경되었다.  

__switch문 String 비교시 컴파일 시점에 hashCode()로 변경된다.__  
글자마다 값이 작은 값부터 정렬한 다음에 String의 equals() 메소드를 사용하여 실제 값과 동일한지 비교한다.  


## 2. 반복문

### 2-1. for문

```Java
// 아래 코드는 매번 반복하면서 list.size() 메소드를 호출하기 때문에 좋지 않다.
for(int i = 0; i < list.size(); i++)

// 떄문에, 아래처럼 사용하는 것이 좋다.
int listSize = list.size();
for(int i = 0; i < listSize; i++)

// 또한, JDK 5부터는 For-Each라고 불리는 개선된 for 루프를 사용할 수 있다.
// 별도의 형변환이나 get(), elementAt() 메소드가 필요 없어 매우 편리하다.
// 단, 이방식은 데이터의 첫 번쨰 값부터 마짐가까지 처리해야 할 경우에만 유용하다.
for(String str: list)
```

*  테스트

for문에서 list.size()를 사용하는 방법,  
미리 list.size() 변수를 정의하고 for문을 반복하는 방법,  
개선된 for문을 사용하는 방법  
총 3가지 방법으로 100,000 번의 반복을 수행하는 테스트를 한다.  
for(listSize 변수 사용): 410 (ms)  
for(list.size() 메소드 사용): 413 (ms)  
for-each: 481 (ms)  

* 결론

10만 번을 반복했기 때문에 차이가 났을 뿐,  
실제 운영중인 웹 시스템에선 이렇게 많이 반복하지 않기 떄문에 별 차이가 없을 것이다.  

__즉, 편리한 방법이나 가독성이 좋은 방식을 사용하는 것이 좋다.__  
__다만, 주의해야 할 점은 반복 구문에서 필요없는 메소드 호출은 피해야 한다.__  

```Java
// TreeSet안에 DataVO[]이 존재한다고 가정한다.

// Bad Case
// toArray(), size() 메소드가 계속해서 반복된다. 이것은 treeSet 크기가 클수록 반복 횟수가 더 늘것이다.
for(int i = 0; i < treeSet.size(); i++) {
	DataVO data = (DataVO) treeSet.toArray()[i];
}

// Goods Case
// toArray(), size() 메소드 모두 한 번만 호출되면 된다. 즉, 크기가 1000이였으면 1번의 호출로 999회를 줄인 것이다.
DataVO[] dataVO = (DataVO) treeSet.toArray();
int treeSetSize = treeSet.size();
for(int i = 0; i < treeSetSize; i++) {
	DataVO data = dataVO[i];
}
```

## 추가적인 키워드

* eqauls()와 hashCode()
* 동등성과 동일성
* https://wikidocs.net/123866: 다양한 switch문 사용 방법, 새로운 switch 구문
* https://jiwondev.tistory.com/113: eqauls(), hashCode(), 동등성, 동일성



