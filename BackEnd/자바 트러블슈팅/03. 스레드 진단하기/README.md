# 스레드 진단하기

## 1. 스레드에서 발생하는 문제들

### 스레드에서 발생하는 문제 중 가장 대표적인 것

스레드에서 일어나는 문제점 중 가장 대표적인 것은 락(Lock)이 발생하는 것이다.  

 - 레이스 컨디션
    - 멀티 쓰레드 환경에서 __하나 이상의 공유 데이터를 처리할 때__ 락 처리를 하지 않을 경우, 동시에 여러 쓰레드에서 데이터를 수정해 버릴 수 있다.
 - 데드락
    - 데이터를 안전하게 처리하기 위해서 거는 락에서 문제가 발생할 수도 있다. **두 개 이상의 쓰레드에서 이 락이 서로 풀리기만을 기다리는 상황**이 발생할 수 있는데, 이것을 데드락이라고 한다.
    - 쓰레드 1이 A 데이터에 락을 건 상태에서 B 데이터를 접근하려고 한다. 이때, 쓰레드 2가 B 데이터에 락을 건 상태에서 A 데이터에 접근하려고 한다. 타이밍이 맞아떨어져서 두 쓰레드가 동시에 요청되어 서로 물고 물리는 상황으로 둘 다 무한정 대기하는 데드락이 발생할 수 있다.
 - 스타베이션
    - 스타베이션은 멈추어 있는 있는 쓰레드가 이론적으로 수행은 할 수 있지만 CPU로부터 일 할 기회를 받지 못하는 경우를 말한다.
    - 쓰레드에는 우선순위라는 것이 있는데, 이러한 __우선순위가 다른 쓰레드보다 낮으면 해당 쓰레드는 스타베이션에 빠질 수 있다.__
 - 라이브 락
    - 하나의 쓰레드에서 다른 쓰레드로 응답을 주고, 응답을 받은 쓰레드에서 요청했던 쓰레드로 다시 __요청 하는 작업이 계속 반복되는 경우__ 를 라이브 락이라고 한다.
    - 데드락은 CPU를 점유하지 않고 멈추어버리지만, 라이브 락은 멈추지 않고 지속해서 수행하므로 CPU까지 점유할 확률이 높다.
 - 다른 형태의 예측 불가능한 오류

### 데드 락 예제 코드

 - synchronized는 객체 고유의 락을 사용한다.
    - synchronized 메서드를 호출하면, 그 메서드를 호출한 객체는 자신의 lock을 획득하게 된다.
    - 한 객체가 synchronized 메서드를 실행하고 있는 동안에는 그 객체에 대해서는 다른 스레드가 그 객체의 synchronized 메서드를 호출할 수 없다.
```java
public class Deadlock {

    public static void main(String[] args) {
        final Friend 홍길동 = new Friend("홍길동");
        final Friend 김철수 = new Friend("김철수");
        new Thread(new Runnable() {
            public void run() {
                김철수.bow(홍길동);
            }
        }).start();
        new Thread(new Runnable() {
            public void run() {
                홍길동.bow(김철수);
            }
        }).start();
    }

    @Getter
    @AllArgsConstructor
    static class Firend {
        private final String name;

        public synchronized void bow(Friend bower) {
            System.out.format("%s: %s has bowed to me!%n", this.name, bower.getName());
            bower.bowBack(this);
        }

        public synchronized void bowBack(Firend bower) {
            System.out.println("%s: %s has bowed back to me!%n", this.name, bower.getName());
        }
    }
}
```

김철수는 bow() 메서드에서 홍길동에게 인사를 한다. 김철수는 자신의 잠금을 획득한 상태이고, 홍길동의 bowBack()을 호출하여 홍길동의 잠금을 기다린다.  
홍길동은 bow() 메서드에서 김철수에게 인사를 한다. 홍길동은 자신의 잠금을 획득한 상태이고, 김철수의 bowBack()을 호출하여 김철수의 잠금을 기다린다.  

### 락 경합을 피하는 10가지 방법

 - 원문 게시글: http://www.thinkingparallel.com/2007/07/31/10-ways-to-reduce-lock-contention-in-threaded-programs/
 - __코드가 아닌 데이터를 보호하라__
    - 데이터만 synchronized 블록으로 감싸는 것으로 중요한 코드를 잠그는 데 수행하는 시간을 줄일 수 있다.
 - __락 사용 부분에서는 비싼 계산을 하지 마라__
    - 재정렬 작업을 짧게 하고 임시 변수를 사용하는 등의 작업으로 락에서 소요하는 시간을 줄인다. 특히 I/O와 관련된 작업이라면 효과가 크다.
 - __락을 분리해라__
    - 사용하는 배열 전체가 동일한 락으로 보호 받아야 하는가? 배열 각각의 요소에 따른 락을 걸 수 있는가?
    - __작업이 너무 많다면, 배열 요소들이 서로 다른 락을 갖도록 분산하고, 쓰레드가 동일한 락을 얻기 위해서 경쟁하지 않도록 만드는 것이 좋다.__
    - 서로 다른 데이터에는 서로 다른 락을 사용한다.
 - __내부적인 락이나 atomic 작업을 사용하라__
    - 카운터 증가를 위해서 락을 사용할 필요는 없다.
    - 만약, 언어 차원에서 atomic 연산을 제공하는 경우 해당 연산을 이용한다.
 - __동기화된 데이터 구조를 사용하라__
    - 만약, atomic 연산을 직접 사용할 수 없다면, 내부적으로 atomic을 사용하는 데이터 구조를 사용할 수 있다. (ex: lock-free 메시지 큐)
 - __가능하다면 읽기-쓰기 락 디자인 패턴을 사용하라__
    - 많은 읽기 작업만 수행하는 사용자들은 동시에 처리할 수 있고, 쓰기 위한 사용자는 락을 걸어서 처리한다. (읽기와 쓰기 분리)
 - __가능하다면 읽기 전용 데이터를 사용하라__
    - 자바를 포함한 몇몇 동시 처리 프로그래밍 시스템은 락을 걸지 않고도 모든 쓰레드에서 접근할 수 잇는 읽기 전용 데이터를 만들 수 있다. (해당 데이터가 전혀 변경되지 않는다는 조건을 만족해야 한다.)
 - __객체 풀링을 피해라__
    - 몇몇 프로그래밍 시스템은 객체를 생성하는 것이 매우 비싸다. 때문에, 객체를 재사용하기 시작했고, 이를 위해 풀(pool)에 저장했다. 동시에 여러 쓰레드가 풀에 접근할 경우 데이터 보호 떄문에 다중 쓰레드에서는 문제가 된다.
    - 풀을 반드시 사용할 필요가 없을 수도 있다.
 - __지역 변수를 사용하거나 쓰레드 로컬 저장소를 사용하라__
    - 쓰레드 로컬은 각 쓰레드마다 별도의 변수를 유지할 수 있도록 하는 Java 클래스이다. ThreadLocal을 사용하면 각 쓰레드가 독립적인 값을 가질 수 있다. remove()를 호출하지 않는 한 쓰레드가 종료될 떄까지 유지된다.
 - __핫스팟을 피하라__
    - 핫스팟은 매우 잦은 변경이 일어나는 리소스 중 하나다.
    - 예시: 리스트 구현체에서 리스트의 크기는 어딘가에 저장되어 있다. 만약, 그렇지 않으면 size() 메서드를 호출할 때마다 일일이 데이터의 크기를 확인해 봐야 하기 떄문에, 데이터의 크기만큼 시간이 소요된다.
        - 리스트의 요소 개수가 변경될 때마다 크기를 저장하는 변수를 수정해야 하고, 그 작업을 수행하는 메서드는 동시 접근을 처리하기 위해 보호되어야 한다. (핫스팟)
        - 이러한 핫스팟을 해결하기 위한 가장 쉬운 방법은 목록의 크기를 저장하지 않는 것이다. 전체 개수를 확인하는 시간은 데이터의 개수가 많을수록 증가한다. (적절한 트레이드 오프 찾기)

### 쓰레드 개수 문제에 대한 권장안

 - __몇 개의  WAS의 스레드 풀을 설정하는 것이 최적인가?__
   - A라는 시스템이 있다고 가정한다. 해당 시스템에서 가장 많이 사용하는 상위 80% URL을 추출하여 성능 테스트를 했다고 가정한다.
   - 테스트를 수행한 결과 50명의 가상 사용자가 최대 처리할 수 있는 사용자로 나왔고 이때의 최대 초당 처리량은 200건이다. 그렇다면 스레드 풀에 최소한 몇 개의 쓰레드를 지정하는 것이 좋은가?
   - 50, 80, 200

50은 최대 처리 가능한 가상 사용자 수를 말한다. 즉, 해당 시스템은 동시에 처리할 수 있는 쓰레드 개수가 50개이다. 60명의 가상 사용자만큼 부하를 준다면, 10명에 해당하는 쓰레드는 어딘가에 대기하게 된다.  

초당 200건을 처리한다는 것은 50명의 가상 사용자의 평균 응답 속도가 0.25초라는 말이 된다. 한 명의 가상 사용자가 0.25초를 소요하니, 1초에 네 번 수행할 수 있다.  

즉, 쓰레드를 200개까지 지정할 필요도 없다. 결론적으로 해당 시스템에 가장 적절한 최소 쓰레드 개수는 50개가 된다. 하지만 상위 80%의 대상에 대해서 테스트를 했다. 나머지 20%가 성능 테스트 시에 병목 지점이 되지 않았던 부분의 로직을 사용할 수도 있다.  

또한, 예상치 못한 사용자의 요청이 대량으로 발생하거나, 추가적인 병목에 사용자들의 요청이 묶일 수도 있다. 때문에, 50개 + 20 ~ 40%로 계산하면 해당 시스템에서는 60 ~ 70개 정도가 적당하다고 볼 수 있다.  

__쓰레드의 개수가 증가하면 증가할수록 쓰레드에서 점유하는 기본 메모리로 인해 애플리케이션에서 가용한 메모리는 점점 줄어든다.__  


## 2. 쓰레드 단면 잘라 놓기

쓰레드 덤프(Thread Dump)는 Java 애플리케이션에서 실행 중인 모든 쓰레드의 상태와 스택 트레이스를 캡처한 스냅샷입니다. 이를 통해 프로그램의 동작 상태를 진단하고, 문제 해결에 도움을 줄 수 있습니다. 쓰레드 덤프는 애플리케이션의 성능 문제, 교착 상태(Deadlock), 과다한 CPU 사용 등과 같은 문제를 분석하는 데 유용합니다.  
 - 모든 시스템이 응답이 없을 때
 - 사용자 수가 많지도 않은데, 시스템의 CPU 사용량이 떨어지지 않을 때
 - 특정 애플리케이션을 수행했는데, 전혀 응답이 없을 때
 - 기타 여러 가지 상황에서 시스템이 내 마음대로 작동하지 않을 때

```java
// javac MakeThreads.java
// java MakeThreads
// java -Xlog:threads MakeThreads
 
import java.util.Map;
import java.util.HashMap;
import java.util.List;
import java.util.ArrayList;

public class MakeThreads {
   public static void main(String[] args) {
      for (int loop = 0; loop < 3; loop++) {
         LoopingThread thread = new LoopingThread();
         thread.start();
      }
      System.out.println("Started looping threads..");
   }
}

class LoopingThread extends Thread {
   public void run() {
      int runCount = 100;

      whilte (true) {
         try {
            String string = new String("AAA");
            List<String> list = new ArrayList<>(runCount);
            for (int loop = 0; loop < runCount; loop++) {
               list.add(string);
            }

            Map<String, Integer> hashMap = new HashMap<>(runCount);
            for (int loop = 0; loop < runCount; loop++) {
               hashMap.put(string + loop, loop);
            }
         } catch (Exception e) {
            e.printStackTrace();
         }
      }
   }
}
```

### 쓰레드 단면

 - 쓰레드 단면 확인
   - jcmd: JDK 7 이후 제공된 도구로, 다양한 JVM 진단 기능 제공
   - jstack: https://docs.oracle.com/en/java/javase/11/tools/jstack.html
```bash
# JVM 실행시 추가 옵션
# -XX:+PrintConcurrentLocks: 각 쓰레드 정보 출력 시 락의 상태 출력
# -XX:+PrintClassHistogram: 클래스별로 점유하고 있는 메모리의 히스토그램
java -XX:+PrintConcurrentLocks -XX:+PrintClassHistogram MakeThreads

# JVM 프로세스 확인
$ jps

# jstack을 사용해 쓰레드 덤프 생성
$ jstack {PID}

# jcmd 명령어 사용
jcmd {PID} Thread.print

# 힙 영역  확인
jstat -gc {PID} {INTERVAL_MS} {INTERVAL_COUNT}
jcmd {PID} GC.heap_info
```

 - 예시 코드
```
2024-10-15 21:29:22
Full thread dump OpenJDK 64-Bit Server VM (11+28 mixed mode):

Threads class SMR info:
_java_thread_list=0x000001bea7fe8cd0, length=13, elements={
0x000001beff35c800, 0x000001beff360000, 0x000001beff3f6800, 0x000001beff3f9000,
0x000001beff3fb000, 0x000001beff400000, 0x000001beff403000, 0x000001beff57a800,
0x000001beff592800, 0x000001beff595000, 0x000001beff596000, 0x000001beff597000,
0x000001bee6bdb800
}

"Reference Handler" #2 daemon prio=10 os_prio=2 cpu=0.00ms elapsed=10.73s tid=0x000001beff35c800 nid=0x9ff8 waiting on condition  [0x0000002a164ff000]
   java.lang.Thread.State: RUNNABLE
        at java.lang.ref.Reference.waitForReferencePendingList(java.base@11/Native Method)
        at java.lang.ref.Reference.processPendingReferences(java.base@11/Reference.java:241)
        at java.lang.ref.Reference$ReferenceHandler.run(java.base@11/Reference.java:213)

"Finalizer" #3 daemon prio=8 os_prio=1 cpu=0.00ms elapsed=10.73s tid=0x000001beff360000 nid=0x9338 in Object.wait()  [0x0000002a165fe000]
   java.lang.Thread.State: WAITING (on object monitor)
        at java.lang.Object.wait(java.base@11/Native Method)
        - waiting on <0x0000000402003070> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(java.base@11/ReferenceQueue.java:155)
        - waiting to re-lock in wait() <0x0000000402003070> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(java.base@11/ReferenceQueue.java:176)
        at java.lang.ref.Finalizer$FinalizerThread.run(java.base@11/Finalizer.java:170)

"Signal Dispatcher" #4 daemon prio=9 os_prio=2 cpu=0.00ms elapsed=10.71s tid=0x000001beff3f6800 nid=0x1864 runnable  [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Attach Listener" #5 daemon prio=5 os_prio=2 cpu=0.00ms elapsed=10.71s tid=0x000001beff3f9000 nid=0x47c8 waiting on condition  [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"C2 CompilerThread0" #6 daemon prio=9 os_prio=2 cpu=31.25ms elapsed=10.71s tid=0x000001beff3fb000 nid=0x8e4c waiting on condition  [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE
   No compile task

"C1 CompilerThread0" #9 daemon prio=9 os_prio=2 cpu=62.50ms elapsed=10.71s tid=0x000001beff400000 nid=0x314 waiting on condition  [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE
   No compile task

"Sweeper thread" #10 daemon prio=9 os_prio=2 cpu=0.00ms elapsed=10.71s tid=0x000001beff403000 nid=0x3e58 runnable  [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Service Thread" #11 daemon prio=9 os_prio=0 cpu=0.00ms elapsed=10.70s tid=0x000001beff57a800 nid=0x9b88 runnable  [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"Common-Cleaner" #12 daemon prio=8 os_prio=1 cpu=0.00ms elapsed=10.69s tid=0x000001beff592800 nid=0x7a8 in Object.wait()  [0x0000002a16dff000]
   java.lang.Thread.State: TIMED_WAITING (on object monitor)
        at java.lang.Object.wait(java.base@11/Native Method)
        - waiting on <0x0000000402000ca8> (a java.lang.ref.ReferenceQueue$Lock)
        at java.lang.ref.ReferenceQueue.remove(java.base@11/ReferenceQueue.java:155)
        - waiting to re-lock in wait() <0x0000000402000ca8> (a java.lang.ref.ReferenceQueue$Lock)
        at jdk.internal.ref.CleanerImpl.run(java.base@11/CleanerImpl.java:148)
        at java.lang.Thread.run(java.base@11/Thread.java:834)
        at jdk.internal.misc.InnocuousThread.run(java.base@11/InnocuousThread.java:134)

"Thread-0" #13 prio=5 os_prio=0 cpu=10640.63ms elapsed=10.69s tid=0x000001beff595000 nid=0x50b4 runnable  [0x0000002a16efe000]
   java.lang.Thread.State: RUNNABLE
        at LoopingThread.run(MakeThreads.java:30)

"Thread-1" #14 prio=5 os_prio=0 cpu=10578.13ms elapsed=10.69s tid=0x000001beff596000 nid=0x8674 runnable  [0x0000002a16ffe000]
   java.lang.Thread.State: RUNNABLE
        at LoopingThread.run(MakeThreads.java:30)

"Thread-2" #15 prio=5 os_prio=0 cpu=10531.25ms elapsed=10.69s tid=0x000001beff597000 nid=0x3424 runnable  [0x0000002a170fe000]
   java.lang.Thread.State: RUNNABLE
        at LoopingThread.run(MakeThreads.java:30)

"DestroyJavaVM" #16 prio=5 os_prio=0 cpu=62.50ms elapsed=10.69s tid=0x000001bee6bdb800 nid=0x5064 waiting on condition  [0x0000000000000000]
   java.lang.Thread.State: RUNNABLE

"VM Thread" os_prio=2 cpu=15.63ms elapsed=10.73s tid=0x000001beff35b800 nid=0x5bac runnable

"GC Thread#0" os_prio=2 cpu=15.63ms elapsed=10.74s tid=0x000001bee6bf4000 nid=0x3110 runnable

"GC Thread#1" os_prio=2 cpu=31.25ms elapsed=10.60s tid=0x000001bea82fd000 nid=0x6590 runnable

"GC Thread#2" os_prio=2 cpu=15.63ms elapsed=10.60s tid=0x000001bea825e000 nid=0x3cf8 runnable

"GC Thread#3" os_prio=2 cpu=15.63ms elapsed=10.60s tid=0x000001bea825e800 nid=0x7488 runnable

"GC Thread#4" os_prio=2 cpu=15.63ms elapsed=10.60s tid=0x000001bea8189800 nid=0x3dd0 runnable

"GC Thread#5" os_prio=2 cpu=15.63ms elapsed=10.60s tid=0x000001bea818a000 nid=0x6154 runnable

"GC Thread#6" os_prio=2 cpu=15.63ms elapsed=10.60s tid=0x000001bea818a800 nid=0x6750 runnable

"GC Thread#7" os_prio=2 cpu=15.63ms elapsed=10.60s tid=0x000001bea818b800 nid=0x2338 runnable

"GC Thread#8" os_prio=2 cpu=15.63ms elapsed=10.60s tid=0x000001bea8127800 nid=0x3e28 runnable

"GC Thread#9" os_prio=2 cpu=15.63ms elapsed=10.60s tid=0x000001bea8124800 nid=0x3af8 runnable

"G1 Main Marker" os_prio=2 cpu=0.00ms elapsed=10.74s tid=0x000001bee6cb0000 nid=0x790c runnable

"G1 Conc#0" os_prio=2 cpu=0.00ms elapsed=10.74s tid=0x000001bee6cb2800 nid=0x9e70 runnable

"G1 Refine#0" os_prio=2 cpu=0.00ms elapsed=10.74s tid=0x000001befea46000 nid=0x8644 runnable

"G1 Young RemSet Sampling" os_prio=2 cpu=0.00ms elapsed=10.74s tid=0x000001befea47000 nid=0x4fcc runnable
"VM Periodic Task Thread" os_prio=2 cpu=0.00ms elapsed=10.70s tid=0x000001beff57b000 nid=0x293c waiting on condition

JNI global refs: 6, weak refs: 0
```

 - 쓰레드 정보
   - 쓰레드 이름
   - 식별자: 데몬 쓰레드일 경우에만 표시 (daemon 이라고 표시)
   - 쓰레드 우선순위(prio): 쓰레드 우선순위를 숫자로 나타낸다. (가장 낮은 것이 1, 높은 것이 10)
   - 쓰레드 ID(tid): 다른 쓰레드와 구분되는 쓰레드의 ID (해당  쓰레드가 점유하는 메모리 주소)
   - 네이티브 쓰레드 ID(nid): OS에서 관리하는  쓰레드의 ID
   - 쓰레드의 상태: 쓰레드 단면을 생성할 때 해당 쓰레드가 하고 있던 작업에 대한 설명
      - NEW: 쓰레드가 아직 시작되지 않은 상태
      - RUNNABLE: 쓰레드가 수행 중인 상태
      - BLOCKED: 쓰레드가 잠겨 있어 풀리기를 기다리는 상태
      - WAITING: 다른 쓰레드가 특정 작업을 수행하여 깨울 때까지 무한정 기다리는 상태
      - TIMED_WAITING: 다른 쓰레드가 특정 작업을 수행하여 깨울 때까지 지정된 시간만큼 기다리고 있는 상태
      - TERMINATED: 쓰레드가 종료된 상태
   - 주소 범위: 쓰레드의 스택 영역의 예상된 주소 범위
```
"Thread-0" prio=6 tid=0x02b1ec00 nid=0xcd8 runnable [0x02e6f000..0x02e6fd94]
  java.lang.Thread.State: RUNNABLE
       at java.util.HashMap.resize(HashMap.java:462)
       at java.util.HashMap.addEntry(HashMap.java:755)
       at java.util.HashMap.put(HashMap.java:385)
       at con.godofjava.thread.LoopingThread.run(MakeThreads.java:28)


"Thread-1" #14 prio=5 os_prio=0 cpu=42140.63ms elapsed=42.92s tid=0x000002a7f8a78800 nid=0x9814 runnable  [0x000000ff109fe000]
   java.lang.Thread.State: RUNNABLE
        at java.util.HashMap.putVal(java.base@11/HashMap.java:635)
        at java.util.HashMap.put(java.base@11/HashMap.java:607)
        at LoopingThread.run(MakeThreads.java:30)
```

## 3. 잘라 놓은 쓰레드 단면 분석하기

ThreadLogic는 Java 쓰레드 덤프를 분석하는 오픈 소스 도구입니다. 이 도구는 주로 Java 애플리케이션의 쓰레드 문제를 진단하고 해결하는 데 도움을 줍니다. Sabha Parameswaran과 Eric Gross가 개발했으며, 이전의 TDA(Thread Dump Analyzer) 도구를 개선한 버전입니다.  
 - ThreadLogic: https://github.com/sparameswaran/threadlogic
   - java -jar ThreadLogic.jar
 - IBM (TMDA): https://www.ibm.com/support/pages/ibm-thread-and-monitor-dump-analyzer-java-tmda
   - java -jar jca4614.jar
 - Fast Thread: https://fastthread.io
   - 웹사이트

### 쓰레드 분석 예시

 - 스레드 목록 확인
 - 잠겨 있는 쓰레드 확인
   - 잠그고 있는 쓰레드와 잠근 쓰레드 때문에 기다리고 있는 다른 쓰레드 목록 확인
 - 무한 루프나 응답 없는 화면 확인
   - CPU 사용량 100%에서 감소되지 않는 경우
   - 쓰레드가 부족하거나, DB Connection Pool 가용 가능한 연결 부족

## 4. 쓰레드 문제 Case Study

시스템이 죽는 경우 쓰레드 단면이 기본적 않는다. 때문에, 문제가 발생했을 때마다 명령어를 수행하도록 하는 OnError나 에러가 발생했을 때 수행되는 스크립트를 정의하는 ErrorFile 옵셔을 줄 수 있다.  

```bash
-XX:OnError="명령어"
-XX:ErrorFile={File Path}
```

### 시스템이 느릴 때도 쓰레드와 관련이 있을까?

시스템이 느리다고 무작정 쓰레드 단면을 뜨는 것은 좋은 해결 방법이라고 할 수 없지만, 생성해 놓으면 뭔가 근거를 찾을 수는 있다. __시스템이 느릴 때에는 다음과 같은 순서로 점거하는 것이 좋다.__  
 - CPU, 메모리와 같은 리소스 사용량 점검
 - 외부와 연동하는 리소스 사용량 점검
 - WAS 메모리 및 쓰레드 설정 및 사용량 점검
 - Web 서버 설정 점검
 - OS 설정 점검
 - 쓰레드 상태 점검
   - APM을 사용하여 프로파일링
   - DB 쿼리가 느린지, DB 서버의 CPU 사용량은 어떤지, DB에 락이 발생하지 않았는지, 다른 외부 연동 서버들의 상태는 괜찮은지
   - __대부분 DB와 같은 WAS와 연동되는 외부 서버들이 원인__
 - 메모리 상태 점검

### 시스템 응답이 없을 때에는 쓰레드 단면이 가장 효과적이다.

__어떤 쓰레드에서 응답을 주지 않아 시스템이 멈추어 버렸는지 매우 쉽게 찾을 수 있는 단서가 된다.__ 보통 WAS가 정해 놓은 쓰레드 풀이나 DB 커넥션 풀이 꽉 찼을 확률이 높다.  
 - __분석 도구 활용시 확인 과정__
   - 전체 쓰레드의 개수 확인
   - JDK 6 이상인 경우 쓰레드 단면의 루트 노드를 클릭하여 메모리 사용량 확인, 여러 개의 단면 파일과 비교해 그 값이 어떻게 변하는지 확인
   - Monitor 목록에서 빨간색으로 표시되어 여러 쓰레드를 잡는 녀석이 없는지 확인
   - 해당하는 쓰레드가 없을 때, Runnable인 쓰레드들을 확인
   - 지속해서 수행 중인 쓰레드가 존재하지 않는지 'Long running threads detect' 기능을 사용하여 확인
   - 그래도 원인이 없어 보인다면 다른 원인 찾아보기
 - __메모리 부족인 경우 확인 과정__
   - 메모리가 부족할 경우 GC 관련 쓰레드가 실행 중인 상태이면서 CPU 코어를 하나 이상 100% 점유하고, 나머지 모든 쓰레드는 아무런 작업을 하지 않을 수 있다.
   - 쓰레드 단면을 주기적으로 떠놓는다.
   - 쓰레드 단면을 뜰 때 'ps -Lf -p pid' 명령어도 같이 수행하여 주기적으로 떠놓는다.
   - 점검한 쓰레드 중 CPU 사용 시간이 지속해서 증가하는 쓰레드가 있다면, 그 쓰레드의 아이디를 확인한 후 쓰레드 단면 분석 도구를 열어 방금 만든 쓰레드 단면에서 해당  쓰레드가 어떤 쓰레드인지 확인해본다.
   - GC 관련 쓰레드라면, 메모리가 부족하거나 GC 알고리즘에 문제가 발생했을 확률이 높다. jstat 명령어로 메모리 사용량을 확인한 후 메모리가 부족하면 메모리 단면을 떠서 어떤 객체가 메모리를 가장 많이 잡고 있는지 확인한다.

### 예외가 지속해서 발생할 때도 쓰레드 단면이 도움이 될까?

__일반적으로 예외가 발생하는 원인은 애플리케이션 코딩상의 실수나 예상치 못한 입력값을 등록하는 것이 대부분이다. 예외가 지속적으로 발생하는 상황에서 스레드 단면의 생성 시 운이 좋아서 예외가 발생하는 그 시점의 상황을 볼 수도 있지만, 스레드 단면으로 많은 결과를 얻기는 힘들다. 이 경우 가장 좋은 단서는 자바의 로그가 찍히는 시스템이다.__

그밖의 이유로 예외 상황이 이어질 수 있는데, 그중 하나가 TimeoutException이다. TimeoutException은 애플리케이션의 설정에 지정해 놓은 Timeout 시간 동안 응답이 없을 때 발생하며, WAT 설정, DB, 각종 외부 연동 시스템에서 응답이 없을 경우에 이러한 예외가 발생할 수 있다. TimeoutException이 지속/반복적으로 발생하는 경우에 그 원인이 DB 쿼리가 느려서인지, GC 때문인지, 아니면 연동되어 있는 시스템에서 응답이 오지 않아 발생하는지에 대해서 확실히 점검해 봐야 한다. 만약, GC 떄문이라면 jstat 명령어나 verbosegc 옵션을 사용하여 확인할 수 있다.

 - 예외가 지속적으로 발생하는 경우 쓰레드 단면으로 많은 결과를 얻기 힘들다. 가장 좋은 것은 로깅하는 것이다.
 - TimeoutException의 원인으로는 WAS 설정, DB, 각종 외부 연동 시스템 응답이 있을 수 있다.

### 사례 1. CPU 사용량이 갑자기 올라가서 안 내려오는 상황

A 시스템에 서버들의 __CPU 사용량이 불규칙적으로 증가한 후 떨어지지 않는 현상이 발생__ 하고 있다.

#### 접근 방법

CPU 사용량이 올라가는 원인은 여러 가지다. CPU 사용량이 올라가면 가장 먼저 확인해야 할 일은 CPU 사용량 점검을 해야하는데, 각 CPU가 어떻게 점유하는지를 확인해야 한다.

 - CPU 사용량이 급증하는 원인
   - 애플리케이션 로직상의 잘못으로 무한 루프에 빠졌을 때
   - XML 라이브러리의 문제로 특수문자가 들어왔을 때 parsing을 제대로 못 하고 무한 루프에 빠졌을 때
   - 정규 표현식을 잘못 사용하여 무한 루프에 빠졌을 때
   - 메모리가 부족하여 GC 관련 쓰레드만 반복적으로 수행하고 있을 때
```bash
# 1. 장애가 발생한 장비에서 스레드 덤프를 30초나 1분 간격으로 5~10회 정도 생성
kill -3 pid

# 2. 스레드 덤프를 생성할 때 동시에 각 스레드별 사용 시간에 대한 덤프도 생성
ps -Lf -p pid

# 3. 스레드 단면 분석 도구로 스레드 덤프 파일을 연다.

# 4. ps 명령어를 사용하여 수집한 덤프에서 수행 시간이 가장 오래 걸린 스레드를 확인한다.

# 5. 스레드 단면 분석 도구에서 해당 스레드에서 어떤 작업을 하고 있는지 스택 정보를 확인해 본다.

# 6. 결과를 고융한다.
```

### 사례 2. 스레드 풀의 스레드 개수가 계속 증가하는 상황

WAS와 같은 멀디 스레드 작업을 하는 프로그램에서는 스레드 풀을 사용한다. DB 연결 풀 처럼 미리 스레드를 생성해 놓고, 그 스레드를 재사용하는 방식이다. 풀을 사용하면 구현이 복잡해지지만, 매번 스레드를 생성할 필요가 없기 때문에 성능이 좋아진다.

#### 상황

B 서비스는 WAS의 스레드 풀을 최대 1,024개로 설정하여 사용하고 있다. 그런데 이 스레드 풀이 꽉 차는 현상이 발생했다. 그런데 특이한 것은 열 대의 장비 중 다른 장비는 이상이 없는데 한 장비에서만 이러한 현상이 발생한다는 것이다.

#### 접근 방법

스레드 개수가 증가하는 상황이기 때문에 스레드 덤프를 뜨는 것이 가장 먼저해야 할 작업이다. 스레드 덤프는 한두 번만 떠서는 안 되며 주기적으로 여러 번 떠야만 한다.

 - 록을 발생시킨 스레드와 대기 스레드 개수
   - A: 405
   - B: 212
   - C: 15
   - D: 10
```
 - A 스택 정보
   - 해당 스레드 단면만 갖고는 분석하기 어렵다.
   - 객체 복사 부분에서 계속 락을 잡고 있는지, 몇 초 뒤에 락이 해제되었는지를 알 수 없다.
   - 해당 장애 시에는 스레드 단면 하나만 있었기 때문에 첫 번째 락이 발생한 원인을 정확히 판단하기 어렵다.
"IP-Processor758" daemon prio=1 tid=0x6b9d7110 nid=0x43a0 waiting on condition [0x497e4000..0x497e4db0]
   at java.lang.Objecet.clone(Native Method)
   at java.util.Arrays.sort(Arrays.java:1079)
   at javax.management.ObjectName.setCanonicalName(ObjectName.java:694)
   at javax.management.ObjectName.construct(ObjectName.java:565)
   at javax.management.ObjectName(ObjectName.java:1304)
   at xxx.jk.common.ChannelSocket.registerRequest(ChannelSocket.java:461)
   at xxx.jk.common.HandlerRequest.checkRequest(HandlerRequest.java:357)
   - locked <0x72dda5e0> (a java.lang.Object)
   at xxx.jk.common.HandlerRequest.decodeRequest(HandlerRequest.java:367)

 - B 스택 정보
   - B, C, D 스레드에서 락이 발생한 원인은 I/O 관련 장비 때문이다. 장비가 노후되어 다른 장비로 교체한 것이엇는데,
   - 만약 해당 장애 상황에서 스레드 정보 외에 시스템의 리소스 정보를 수집해 놓았다면 조금 더 빨리 찾았을 것이다.
   - 장애 발생시 애플리케이션상의 문제가 아닌 다른 원인 떄문에도 발생할 수 있다.
"IP-Processor244" daemon prio=1 tid=0x67476000 nid=0x3d7c waiting for monitor entry [0x59ae1000..0x59ae6eb0]
   // 중간 생략
   at java.security.AccessController.checkPermission(AccessController.java:427)
   at java.lang.SecurityManager.checkPermission(SecurityManager.java:532)
   at java.lang.SecurityManager.checkRead(SecurityManager.java:871)
   at java.io.File.lastModified(File.java:793)

C 스택 정보
"IP-Processor299" daemon prio=1 tid=0x64ddc9e8 nid=0x3df1 waiting for monitor entry [0x57f2c000..0x57f30030]
   at sun.net.www.ParseUtil.decode
   at sun.net.www.protocol.file.Handler.openConnection
   - lock <0x72e7b880>
   // 중간 생략
   at java.lang.SecurityManager.checkPermission(SecurityManager.java:532)
   at java.lang.SecurityManager.checkRead(SecurityManager.java:871)
   at java.io.File.lastModified(File.java:793)

D 스택 정보
"IP-Processor456" daemon prio=1 tid=0x64ddc9e8 nid=0x3df1 waiting for monitor entry [0x57f2c000..0x57f30030]
   at sun.nio.cs.FastCharsetProvidere.toLower
   at sun.nio.cs.FastCharsetProvider.lookup
   - lock <0x730c6f90>
   // 중간 생략
   at java.lang.SecurityManager.checkRead(SecurityManager.java:871)
   at java.io.File.exists(File.java:700)

```

### 사례 3. 시스템 응답이 없는 상황

C 시스템의 WAS가 응답을 하지 않는다. 이 서비스를 제공 하는 대부분의 서버가 이러한 상황이다. 각 서버의 CPU는 하나만 줄기차게 사용하고 있으며, 스레드 덤프와 ps -Lf 명령어를 사용하여 어떤 스레드가 CPU를 계속 사용하고 있는지에 대한 자료는 모아 두었다.

#### 접근 방법

 - ps -Lf 명령어로 수집한 데이터
   - ps -Lf 명령어는 프로세스와 스레드 정보를 보여준다.
   - 2252, 2253 숫자를 가진 스레드가 지금도 사용중이고 매우 오랜 시간 동안 수행되어 온 것을 확인할 수 있다.
```bash
# UID: 프로세스를 실행한 사용자의 ID. 사용자 이름을 의미합니다.
# PID: 프로세스 ID. 각 프로세스에 부여된 고유한 번호입니다.
# LWP: Lightweight Process ID, 즉 스레드 ID. 이 값은 특정 프로세스 내에서 개별 스레드를 구별하는 데 사용됩니다.
UID        PID  PPID   LWP  C NLWP    STIME TTY      TIME CMD
userid    2250     1  2250  0  608  Sep15  ?        00:00:00 java ...
userid    2250     1  2252  0  608  Sep15  ?        00:00:06 java ...
userid    2250     1  2253  0  608  Sep15  ?        06:12:00 java ...
..
```

 - 스레드 단면 분석 요구 활용
   - Native ID 확인한다.
   - CPU를 혼자 점유하고 있는 것은 GC 관련 스레드였다.
   - 이러한 상황에서 장애를 발생시킨 가장 유력한 용의자는 바로 메모리 릭이다.
```bash
"Gang worker#0 (Parallel GC Threads)" prio=10 tid=0x0040118800 nid=0x8cd runnable
"Gang worker#1 (Parallel GC Threads)" prio=10 tid=0x004011a800 nid=0x8ce runnable
```

