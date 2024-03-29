# 리눅스 소개

## 리눅스의 역사

리눅스(Linux)는 현대 컴퓨터 운영 체제의 하나로, 다중 사용자, 다중 작업, 네트워크 운용이 가능한 오픈 소스 Unix 계열 운영 체제입니다. 리눅스는 오픈 소스 소프트웨어로서, 누구나 자유롭게 사용하고 수정할 수 있습니다. 이 운영 체제는 커널이라는 핵심 부분과 여러 가지 유틸리티 및 시스템 소프트웨어로 구성되어 있습니다.  

리눅스의 역사는 1991년 핀란드의 대학생인 리누스 토발즈(Linus Torvalds)가 처음으로 리눅스 커널을 개발한 것으로부터 시작됩니다. 그 당시에는 아주 간단한 커널로 시작했지만, 인터넷을 통해 다른 프로그래머들의 협력을 받아 점차 발전하게 되었습니다. 리눅스는 개발자들의 자발적인 기여와 협업을 통해 지속적으로 발전하고 있습니다.  

 - __1990년대__
    - 1991년: 리누스 토발즈가 처음으로 리눅스 커널을 개발하고 인터넷에 공개합니다.
    - 1992년: GNU 프로젝트의 유틸리티와 GNU General Public License(GPL)을 채택하여 리눅스가 오픈 소스 소프트웨어로 정의됩니다.
    - 1993년: 리눅스 개발자들이 커널 개발을 조직화하기 위해 '리눅스 커널 Mailing List'를 만듭니다.
    - 1994년: 첫 번째 리눅스 배포판인 "Slackware"가 출시됩니다.
    - 1996년: 리눅스 개발자들이 "Linux Standard Base (LSB)"를 만들어 리눅스 배포판의 표준화를 시도합니다.
 - __2000년대__
    - 2000년대 초반: 리눅스는 서버 환경에서 점차 더 많이 사용되기 시작합니다.
    - 2001년: IBM이 리눅스를 지원하기 위해 1억 달러를 투자합니다.
    - 2003년: 리눅스 커뮤니티에서 개발된 서버 배포판인 "Red Hat Enterprise Linux"과 "SUSE Linux Enterprise Server"가 출시됩니다.
    - 2005년: 리눅스 개발에 대한 기여를 촉진하기 위해 "Linux Foundation"이 설립됩니다.
    = 2008년: 안드로이드 플랫폼이 리눅스 기반으로 개발되어 출시됩니다.
 - __2010년대__
    - 2011년: 리눅스 커널 3.0 버전이 출시됩니다.
    - 2012년: 리눅스가 세계적으로 널리 사용되는 기업 환경에서 인식되고, 많은 기업이 리눅스를 채택합니다.
    - 2013년: 안드로이드가 스마트폰 시장에서 압도적인 지분을 차지하며 리눅스의 모바일 시장에서의 영향력이 커집니다.
    - 2015년: Microsoft가 리눅스 커뮤니티와의 협력을 강화하며 Windows 서버에서 리눅스 기능을 지원합니다.
    - 2019년: 리눅스는 클라우드 컴퓨팅에서 주류 운영 체제로 강세를 보이며, AWS, Google Cloud Platform, Microsoft Azure 등의 클라우드 서비스에서 널리 사용됩니다.

<br/>

## 운영체제

운영 체제(Operating System, OS)는 컴퓨터 시스템에서 하드웨어와 응용 소프트웨어 간의 인터페이스를 제공하고 관리하는 소프트웨어입니다. 컴퓨터의 핵심 부분으로, 사용자 및 응용 프로그램이 하드웨어 자원을 효율적으로 활용할 수 있도록 돕습니다.  

 - 메모리 관리, 인터럽트 처리, I/O 디바이스와의 통신, 파일 관리, 네트워크 스택 구성 관리 등 처리
 - 자원 관리(Resource Management): 운영 체제는 컴퓨터의 자원인 CPU, 메모리, 저장 장치, 네트워크 등을 관리합니다. 이를 효율적으로 할당하여 다양한 응용 프로그램이 동시에 실행될 수 있도록 합니다.
 - 프로세스 관리(Process Management): 프로세스는 실행 중인 프로그램을 의미하며, 운영 체제는 이러한 프로세스를 생성, 중단, 일시 중단 및 관리합니다.
 - 파일 시스템 관리(File System Management): 파일 시스템은 데이터를 저장하고 구성하는 방법을 관리합니다. 운영 체제는 파일 및 디렉토리의 생성, 삭제, 읽기 및 쓰기와 같은 파일 시스템 작업을 처리합니다.
 - 입출력 관리(Input/Output Management): 입출력 장치와의 상호 작용을 관리합니다. 이는 키보드, 마우스, 모니터, 프린터 및 네트워크와 같은 외부 장치와의 통신을 포함합니다.
 - 사용자 인터페이스 제공(User Interface): 운영 체제는 사용자와 컴퓨터 간의 상호 작용을 지원하는 사용자 인터페이스를 제공합니다. 이는 명령 줄 인터페이스(Command Line Interface, CLI)나 그래픽 사용자 인터페이스(GUI) 형태일 수 있습니다.

<br/>

## 리소스 가시성

리소스란 소프트웨어 실행을 지원하는 데 사용할 수 있는 모든 것으로 간주할 수 있다. 하드웨어와 그 추상화(CPU, RAM, 파일 등), 파일 시스템, 하드 디스크 드라이브, SSD, 프로세스, 디바이스나 라우팅 테이블 같은 네트워킹 관련 항목, 사용자를 나타내는 자격증명 등이 포함된다.  

```bash
# 리눅스 버전 조회
$ cat /proc/version

# 사용 중인 CPU의 특정 하드웨어 정보 조회
$ cat /proc/cpuinfo | grep "model name"
```
<br/>

리눅스는 프로세스 ID(PID)를 사용해 프로세스를 식별한다.  
 - 기본적으로 프로세스 ID는 고유해야 한다. 하지만, 네임스페이스라고 하는 서로 다른 컨텍스트에는 동일한 PID를 가진 여러 프로세스가 있을 수 있다.
 - 모든 프로세스는 PID 1을 특별하게 사용한다. 전통적인 설정에서 PID 1은 사용자 공간 프로세스 트리의 루트용으로 예약되어 있다.
 - 리눅스에서는 cgroup이라는 커널 기능을 사용해 프로세스 간의 격리를 제공한다.

