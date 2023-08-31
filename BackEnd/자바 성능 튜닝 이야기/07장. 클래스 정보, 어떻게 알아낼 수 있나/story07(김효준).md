# 07. 클래스 정보 어떻게 알아낼 수 있나?

* 1. Reflection

## 1. Reflection

```
나초보씨는 메소드의 로그 부분을 작성하면서 매번 클래스의 이름을 지정하는 것이 귀찮아졌다.
클래스의 정보를 얻는 방법이 없을까?
```

* 리플렉션(Reflection)

컴퓨터 과학 용어로 리플렉션(Reflection)은 컴퓨터 프로그램에서 런타임 시점에 사용되는 자신의 구조와 행위 관리하고 수정할 수 있는 프로세스를 의미합니다.  
즉, 리플렉션은 런타임(runtime)에 실행 중인 프로그램의 내부 구조를 분석하고 조작할 수 있는 기능입니다.  
Reflection을 사용하면 프로그램이 자신의 클래스, 필드, 메서드, 생성자 등에 대한 정보를 동적으로 얻을 수 있으며, 이를 통해 해당 클래스 또는 객체를 조작하거나 실행할 수 있습니다.  
※ 추가적으로 C, C++ 에서는 리플렉션(Reflection) 기능이 존재하지 않는다.  

* Java Reflection

Java에서는 java.lang.reflection 패키지로 리플렉션 주요 클래스를 제공한다.  
해당 패키지에 있는 클래스들을 사용하면 JVM에 로딩되어 있는 클래스와 메소드 정보를 읽어올 수 있다.  

```Java
// 1. Class 클래스
String getName(): 클래스의 이름을 리턴한다.
Package getPackage(): 클래스의 패키지 정보를 패키지 클래스 타입으로 리턴한다.
Field[] getFields(): public으로 선언된 변수 목록을 Field 클래스 배열 타입으로 리턴한다.
Field getField(String name): public으로 선언된 변수를 Field 클래스 타입으로 리턴한다.
Field[] getDeclaredFields(): 해당 클래스에서 정의된 변수 목록을 Field 클래스 배열 타입으로 리턴한다.
Field getDeclaredField(String name): name과 동일한 이름으로 정의된 변수를 Field 클래스 타입으로 리턴한다.
Method[] getMethods(): public으로 선언된 모든 메소드 목록을 Method 클래스 배열 타입으로 리턴한다. 해당 클래스에서 사용 가능한 상속 받은 메소드도 포함된다.
Method getMethod(String name, Class... parameterTypes): 지정된 이름과 매개변수 타입을 갖는 메소드를 Method 클래스 타입으로 리턴한다.
Method[] getDeclaredMethods(): 해당 클래스에서 선언된 모든 메소드 정보를 리턴한다.
Method getDeclaredMethod(String name, Class... parameterTypes): 지정된 이름과 매개변수 타입을 갖는 해당 클래스에서 선언된 메소드를 Method 클래스 타입으로 리턴한다.
Constructor[] getConstructors(): 해당 클래스에 선언된 모든 public 생성자 정보를 Constructor 배열 타입으로 리턴한다.
Constructor[] getDeclaredConstructors(): 해당 클래스에서 선언된 모든 생성자의 정보를 Constructor 배열 타입으로 리턴한다.
int getModifiers(): 해당 클래스의 접근자(modifier) 정보를 int 타입으로 리턴한다.
String toString(): 해당 클래스 객체를 문자열로 리턴한다.

// 2. Method 클래스
Class<?> getDeclaringClass(): 해당 메소드가 선언된 클래스 정보를 리턴한다.
Class<?> getReturnType(): 해당 메소드의 리턴 타입을 리턴한다.
Class<?>[] getParameterTypes(): 해당 메소드를 사용하기 위한 매개변수의 타입들을 리턴한다.
String getName(): 해당 메소드의 이름을 리턴한다.
int getModifiers(): 해당 메소드의 접근자 정보를 리턴한다.
Class<?>[] getExceptionTypes(): 해당 메소드에 정의되어 있는 예외 타입들을 리턴한다.
Object invoke(Object obj, Object... args): 해당 메소드를 수행한다.
String toGenericString(): 타입 매개변수를 포함한 해당 메소드의 정보를 리턴한다.
String toString(): 해당 메소드의 정보를 리턴한다.

// 3. Field 클래스
int getModifiers(): 해당 변수의 접근자 정보를 리턴한다.
String getName(): 해당 변수의 이름을 리턴한다.
String toString(): 해당 변수의 정보를 리턴한다.
```

* 테스트

```Java
@allargsconstructor
@Getter
@Setter
public class DataVO {
	private String name;
	private String age;
}

public static void main(String[] args) {
	Object data = new DataVO("김효준", "27");
	
	printClassInfo(data);
	printMethodInfo(data);
	printFieldInfo(data);
}

public static void printClassInfo(Object clazz) {
	Class myClass = clazz.getClass();
	
	// 클래스명 조회
	System.out.println(myClass.getName()); // 패키지명.클래스명
	System.out.println(myClass.getSimpleName()); // 클래스명
	
	// 패키지명 조회
	System.out.println(myClass.getPackageName());
	System.out.println(myClass.getPackage().getName());
}

public static void printMethodInfo(Object clazz) {
	Class myClass = clazz.getClass();
	
	Method[] methodArray = myClass.getDeclaredMethods();
	for(Method method: methodArray) {
		String methodName = method.getName();
		String modifierStr = Modifier.toString(method.getModifiers());
		String returnType = method.getReturnType().getSimpleName();
		Class params[] = method.getParameterTypes();
		String paramStr = convertClassArrayToString(params);
		
		System.out.printf("%s %s %s(%s)\n", modifierStr, returnType, methodName, paramStr);
	}
}

public static String convertClassArrayToString(Class[] params) {
	StringBuilder sb = new StringBuilder();
	int paramsLength = params.length;
	for(int i = 0; i < paramsLength; i++) {
		if(i == 0) {
			sb.append(params[i].getSimpleName()).append(" arg");
		}
		sb.append(", ").append(params[i].getSimpleName()).append(" arg");
	}
	return sb.toString();
}

public static void printFieldInfo(Object clazz) {
	Class myClass = clazz.getClass();
	
	Field[] fieldArray = myClass.getDeclaredFields();
	for(Field field: fieldArray) {
		String fieldName = field.getName();
		String modifierStr = Modifier.toString(field.getModifiers());
		String type = field.getType().getSimpleName();
		System.out.printf("%s %s %s\n", modifierStr, type, fieldName);
	}
}
```

* 결론

__리플렉션 기능을 사용하면 런타임에 동적으로 클래스, 필드, 메소드, 생성자 등의 정보를 얻을 수 있다.__  
__리플렉션은 런타임에 클래스를 분석하므로 속도가 느리기 때문에 정말 필요한 곳에서만 리플렉션을 한정적으로 사용해야 한다.__  

※ 추가적으로 책에서 명시된 Perm 영역은 JDK 7버전 이전에 존재하던 영역으로 GC 대상이 아니여서 많이 쌓이게 되면 OutOfMemoryError가 발생할 수 있었다.  
※ JDK 8 이후부터는 해당 문제에 대해서 신경쓰지 않아도 된다.  

```Java
// 1. 잘못 사용한 예시: 리플렉션을 이용하여 자료형 체크 후 데이터 처리
if(object.getClass().getName().equals("java.math.BigDecimal")) {
    // 데이터 처리
    ..
}

// 2. 잘 사용한 예시: instanceof를 이용하여 자료형 체크 후 데이터 처리
if(object instanceof java.math.BigDecimal)) {
    // 데이터 처리
    ..
}
```

## 추가적인 키워드

* Perm 영역
* Metaspace 영역
* https://jaehoney.tistory.com/177: Perm, Metaspace
