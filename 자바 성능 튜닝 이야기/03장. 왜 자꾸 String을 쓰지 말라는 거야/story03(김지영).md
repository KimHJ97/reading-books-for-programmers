# Story 3. 왜 자꾸 String을 쓰지 말라는 거야

int, long 같은 기본 자료형을 제외하면,

가장 많이 사용하는 객체 1위는 String, 2위는 Collection 관련 클래스이다.

String은 GC에 영향을 주는 것은 확실하다. 

하지만 이것만 고친다고 애플리케이션의 메모리가 효율적으로 사용된다는 것은 아니다.

 성능 개선에 있어 작은 부분이지만 이것부터 적용하라는 의미이다.

String VS StringBuffer VS StringBuilder

예제 

10,000회 반복하여 문자열을 더하고 이러한 작업을 10회 반복한다.

그리고 이 화면을 10회 반복 호출한다.

실행결과

|  | 주요 소스 부분 | 응답 시간 | 메모리 사용량 |
| --- | --- | --- | --- |
| String | a+=aValue | 95초 | 약 95Gb |
| StringBuffer | b.append(aValue); | 0.24초 | 약 28Mb |
| StringBuilder | c.append(aValue); | 0.17초 | 약 9.5Mb |

응답시간은 String 보다 StringBuffer가 약 367배 빠르며, StringBuilder가 512배 빠르다.

메모리는 String이 3,390배 더 사용한다.

a에 aValue를 더하는 과정에서 String은 새로운 String 클래스 객체가 만들어지고,

이전 a 객체는 필요 없는 값이 되어 GC에 대상이 된다.

반면 StringBuffer나 StringBuilder는 새로운 객체를 생성하지 않고 기존의 객체에 값을 더한다.

이런 작업이 반복수행되면서 메모리를 많이 사용하고 응답 속도에도 많은 영향을 미치게 된다.

GC를 하면 할수록 시스템의 CPU를 사용하고 시간도 많이 소요된다.

그래서 프로그래밍을 할때 메모리 사용을 최소화하는 것은 당연한 일이다.

- String은 짧은 문자열을 더할 경우 사용한다.
- StringBuffer는 스레드에 안전한 프로그램이 필요할 때나 개발 중인 시스템이 스레드에 안전한지 모를 경우 사용하면 좋다. 만약 클래스에 static으로 선언한 문자열을 변경하거나, singleton으로 선언된 클래스에 선언된 문자열일 경우에 사용해야 한다.
- StringBuilder는 스레드에 안전한지의 여무와 전혀 관계없는 프로그램을 개발할때 사용하면 좋다. 만약 메서드 내에 변수를 선언했다면, 해당 변수는 그 메서드 내에서만 살았으므로 StringBuilder를 사용하면 된다.

JDK 5.0 이후에는 String으로 문자열을 더했다면 컴파일러에서 자동으로 StringBuilder로 변환해 준다.

하지만 반복 루프를 사용해서 문자열을 더할때는 객체를 계속 추가하므로 String는 사용하지 않는 것이 좋다.

---

StringBuffer(CharSequence seq) : CharSequence를 매개변수로 받는 생성자

CharSequence는 인터페이스이다.

구현한 클래스로는 CharBuffer, String, StringBuffer, StringBuilder가 있다.

StringBuffer, StringBuilder로  값을 만든 후 굳이 toString을 수행하여 필요없는 객체를 만들어서 넘겨주기 보다는 CharSequence로 받아서 처리하는 것이 메모리 효율에 더 좋다.