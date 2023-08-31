# story 18

# GC가 어떻게 수행되고 있는지 보고싶다

## 자바 인스턴스 확인을 위한 jps

jps는 해당 머신에서 운영중인 JVM의 목록을 보여줌

사용법 : `jps [-q] [-mlvV] [-Joption] [<hostid>]`

커맨드 창에서 아무 옵션 없이 jps를 입력하면 현재 서버에서 수행되고 있는 자바 인스턴스들의 목록이 나타남

## GC 상황을 확인하는 jstat

GC가 수행되는 정보를 확인하기 위한 명령어

jstat을 사용하면 유닉스 장비에서 vmstat나 netstat와 같이 라인 단위로 결과를 보여줌

`jstat -<option> [-t] [-h<lines>] <vmid> [<interval> [<count>]]`

### jstat 명령 옵션

- -t : 수행 시간 표시( 수행 시간 : 해당 자바 인스턴스가 생성된 시점부터의 시간)
- -h:lines : 각 열의 설명을 지정된 라인 주기로 표시
- interval : 로그를 남기는 시간의 차이를 의미
- count : 로그 남기는 횟수를 의미

option의 종류

- gccapacity : 각 영역의 허용치와 연관된 영역에 대한 통계
- gcnew : 각 영역에 대한 통계
- gcutil : GC에 대한 요약 정보

**적용 예시**

jstat -gcnew -t -h10 2624 1000 20 > jstat_WAS1.log

- gcnew : 각 영역에 대한 통계를 보여줌
- t : 수행 시간을 나타냄
- h10 : 10줄에 한번씩 각 열의 설명을 나타냄
- 2624 : 프로세스 번호
- 1000 : 1초(1000ms)에 한번씩 정보를 보여줌
- 20 : 20회 반복 수행
- > jstat_WAS1.log : jstat_WAS1.log 파일에 결과 저장

**정리**

- jstat의 결과를 사용하여 그래프를 그리면 GC 추이를 볼 수 있으므로 편리함
- 결과를 파일로 남길 수 있어 나중에 분석할 때 사용 가능
- 단, 이 결과로는 어떻게 해석하면 좋을지 알기 어려움
- JVM 파리미터 튜닝, GC를 수행하는데 소요된 모든 시간을 보고싶을 때 유용함
- jstat으로 분석하는건 로그를 남기는 주기에 GC가 한번 발생할 수도, 10번 발생할 수도 있기 때문에 한계가 있음 ⇒ 뒤의 verbosegc 옵션 사용을 권장

## GC 튜닝할 때 가장 유용한 jstat 옵션

1. gccapacity
    
    현재 각 영역에 할당되어 있는 메모리의 크기를 KB 단위로 나타냄
    
    사용법 : jstat -gccapacity 3580
    
    3580은 프로세스의 pid
    
    **결과**
    
    NGC로 시작하는 것은 New(Young) 영역의 크기 관련
    
    OGC로 시작하는 것은 Old 영역 크기 관련
    
    PGC로 시작하는 것은 Perm 영역 크기 관련 정보
    
    S0C, S1C, EC, OC, PC 는 각각 Servivor0, Servivor1, Eden, Old, Perm 영역의 현재 할당된 크기
    
    MN, MX, C로 끝나는 항목들은 각각 Min, Max, Committed를 나타냄
    
    가장 끝에 YGC, FGC는 각각 Minor GC 횟수, Full GC 횟수를 의미
    
    **장점**
    
    - 각 영역의 크기를 알 수 있기 때문에 어떤 영역의 크기를 늘리고, 줄여야 할 지 확인할 수 있음
    - 이 명령어만 수행해 보면 해당 자바 프로세스의 메모리 점유 상황을 쉽게 확인 가능
    
2. gcutil
    
    힙 영역의 사용량을 %로 보여줌
    
    사용법 : jstat -gcutil 3580 1s
    
    결과
    
    S0, S1은 Survivor 영역을 의미
    
    E는 Eden
    
    YGC는 Young 영역의 GC 횟수, YGCT는 Young 영역의 GC가 수행된 누적 시간
    
    O는 Old, P는 Perm 영역을 의미하며, 이 두개 영역 중 하나라도 GC가 발생하면 FGC의 횟수가 증가하고, FGCT 시간이 올라감
    
    GCT는 Young GC가 수행된 시간인 YGCT와 Full GC가 수행된 시간인 FGCT의 합
    
    ## 원격으로 JVM 상황을 모니터링하기 위한 jstatd
    
    이 명령어를 사용하면 원격 모니터링이 가능
    
    바로 실행하면 자바에 기본적으로 지정되어 있는 보안 옵션이 jstatd가 리모트 객체를 만드는 것을 억제하기 때문에 오류 발생
    
    ⇒ 자바가 설치된 서버 내 디렉터리의 lib/security/java.policy 파일에 허가 명령어 추가
    
    jstatd를 통해 ‘호스트명:포트번호’를 지정하면 원격으로 jstat 명령을 수행하여 결과 확인 가능
    
    ## verbosegc 옵션을 이용하여 gc 로그 남기기
    
    자바 수행 시에 -verbosegc 옵션을 넣어서 사용
    
    ### PrintGCTimeStamps 옵션
    
    verbosegc 옵션과 함께 사용할 수 있는 옵션
    
    서버가 기동되기 시작한 이후부터 해당 GC가 수행될 때까지의 시간을 로그에 포함하기 때문에 언제 GC가 발생되었는지 확인할 수 있음
    
    ### PrintHeapAtGC 옵션
    
    GC에 대한 더 많은 정보를 볼 수 있음
    
    GC가 한 번 수행될 때 각 영역에서 얼마나 많은 메모리 영역을 사용하고 있는지 상세하기 볼 수 있음
    
    ### PrintGCDetails
    
    PrintHeapAtGC 보다 더 간결하고 보기 쉬운 옵션
    
    ### 각 서버에 알맞은 분석 툴
    
    GC Analyzer, IBM GC 분석기, HPjtune