# 02장. 스프링 배치

## 배치 아키텍처

스프링 배치 프레임워크는 3가지 레이어인 애플리케이션 레이어, 코어 레이어, 인프라스트럭처 레이어가 존재한다.  
애플리케이션 레이어는 개발자가 개발한 코드를 나타내며, 대부분 코어 레이어와 상호 작용을 한다.  
코어 레이어는 배치 영역을 구성하는 실제적인 여러 컴포넌트로 이루어져 있다.  
인프라스트럭처 레이어는 ItemReader 및 ItemWrite를 비롯해, 재시작과 관련된 문제를 해결할 수 있는 클래스와 인터페이스를 제공한다.  
 - 애플리케이션 레이어: 개발자가 작성한 모든 배치 작업과 사용자 정의 코드 포함
 - 코어 레이어: 배치 작업을 시작하고 제어하는데 필요한 핵심 런타임 클래스 포함 (JobLauncher, Job, Step 등)
 - 인프라스트럭처 레이어: 개발자와 애플리케이션에서 사용하는 일반적인 Reader와 Writer

<div align="center">
    <img src="./images/spring-batch-layers.png">
</div>


<br/>

## 잡과 스텝

__잡(Job)__ 은 배치처리 과정을 하나의 단위로 만들어 놓은 객체입니다. 또한 배치처리 과정에 있어 전체 계층 최상단에 위치하고 있습니다.  
__스텝(Step)__ Job의 배치처리를 정의하고 순차적인 단계를 캡슐화 합니다. Job은 최소한 1개 이상의 Step을 가져야 하며 Job의 실제 일괄 처리를 제어하는 모든 정보가 들어있습니다.  
스텝은 잡을 구성하는 독립된 작업의 단위로, 태스크릿(Tasklet) 기반 스텝과 청크(Chunk) 기반 스텝이라는 2가지 유형이 있다.  
__태스크릿 기반 스텝__ 은 Tasklet을 구현하며, 스텝이 중지될 때까지 execute 메서드가 계속 반복해서 수행된다. 태스크릿 기반 스텝은 초기화, 저장 프로시저 실행, 알림 전송 등과 같은 잡에서 일반적으로 사용된다.  
__청크 기반 스텝__ 은 ItemReader, ItemProcessor, ItemWriter라는 3개의 주요 부분으로 구성될 수 있다. 여기서 ItemReader와 ItemWriter는 필수이고, ItemProcessor는 필요시에 구성할 수 있다.  
 - org.springframework.batch.core.Job: ApplicationContext 내에 구성되는 잡 객체
 - org.springframework.batch.core.Step: ApplicationContext 내에 구성되는 스텝을 나타내는 객체
 - org.springframework.batch.core.step.tasklet.Tasklet: 트랜잭션 내에서 로직이 실행될 수 있는 기능을 제공하는 전략(strategy) 인터페이스
 - org.springframework.batch.item.ItemReader<T>: 스텝 내에서 입력을 제공하는 전략 인터페이스
 - org.springframework.batch.item.ItemProcessor<T>: 스텝 내에서 제공받은 개별 아이템(Item)에 업무 로직, 검증 등을 적용하는 역할을 하는 인터페이스
 - org.springframework.batch.item.ItemWriter<T>: 스텝 내에서 아이템을 저장하는 전략 인터페이스

<div align="center">
    <img src="./images/spring-batch-reference-model.png">
</div>

<br/>

## 잡 실행

잡이 실행될 때 스프링 배치의 많은 컴포넌트는 탄력성을 제공하기 위해 서로 상호작용을 한다.  
__JobRepository__ 컴포넌트는 다양한 배치 수행과 관련된 수치 데이터(시작 시간, 종료 시간, 상태, 읽기/쓰기 횟수 등)뿐만 아니라 잡의 상태를 유지 관리한다. JobRepository는 일반적으로 관계형 데이터베이스를 사용하며 스프링 배치 내의 대부분의 주요 컴포넌트가 공유한다.  
__JobLauncher__ 는 잡을 실행하는 역할을 담당한다. Job.execute 메서드를 호출하는 역할 이외에도, 잡의 재실행 가능 여부 검증, 잡의 실행 방법, 파라미터 유효성 검증 등의 처리를 수행한다.  

잡을 실행하면 해당 잡은 각 스텝을 실행한다. 각 스텝이 실행되면 JobRepository는 현재 상태로 갱신된다.  
즉, 실행된 스텝, 현재 상태, 읽은 아이템 및 처리된 아이템 수 등이 모두 JobRepository에 저장된다.  

<br/>

## 병렬화

단순한 배치 처리 아키텍처는 잡 내의 스텝을 처음부터 끝까지 순서대로 단일 쓰레드에서 실행하는 것이다.  
스프링 배치는 다양한 병렬화 방법을 제공한다. 잡을 병렬화하는 방법에는 다중 쓰레드 스텝을 통한 작업 분할, 전체 스텝의 병렬 실행, 비동기 ItemProcessor/ItemWriter 구성, 원격 청킹, 파티셔닝 5가지 방법이 있다.  

 - `다중 쓰레드 스텝`

스프링 배치에서 잡은 청크라는 블록 단위로 처리되도록 구성되며, 각 청크는 각자 독립적인 트랜잭션으로 처리된다.  
일반적으로 각 청크는 연속해서 처리되는데, 10,000개의 레코드가 있을 때 커밋 수를 50개로 설정했다면 잡은 레코드 1부터 50까지를 처리한 다음에 커밋하고, 51부터 100까지 처리하고 커밋하고, 이 과정을 10,000 레코드가 모두 처리될 때까지 반복한다.  
스프링 배치를 사용하면 작업을 병렬로 실행해 성능을 향상시킬 수 있다.  

 - `병렬 스텝`

입력 파일의 데이터를 읽어오는 한 개의 스텝과 데이터베이스에 저장하는 일을 하는 한 개의 스텝이 있고, 서로 관련이 없다고 가정한다.  
이떄, 파일 하나를 전부 불러와 저장을 완료하기까지 다른 파일의 처리를 미루고 기다릴 필요가 없다.  
이런 경우 병렬 스텝 처리 기능을 이용할 수 있다.  

 - `비동기 ItemProcessor/ItemWriter`

ItemReader가 제공하는 데이터를 가공하기 위해 복잡한 수학 계산을 수행하거나 원격 서비스를 호출해야하는 경우가 있다. 이러한 경우 일부 스텝을 병렬화하는 기능을 사용할 수 있다.  
SynchonousItemProcessor는 ItemProcessor가 호출될 때마다 동일한 쓰레드에서 실행하게 만들어주는 ItemProcessor 구현체의 데코레이터이다. ItemProcessor 호출 결과를 반환하는 대신, 각 호출에 대해 java.utilconcurrent.Future를 반환한다. 현재 청크 내에서 반환된 Future 목록은 AsynchronousItemWriter로 전달된다.  

 - `원격 청킹`

원격 청킹 방식에서 입력은 마스터 노드에서 표준 ItemReader를 사용해 이루어진다.  
그런 다음 입력은 지속 가능한 통신 형식(RabbitMQ, ActiveMQ 등 메시지 브로커)을 통해 메시지 기반 POJO로 구성된 원격 워커 ItemProcessor로 전송된다.  
처리가 완료되면 워커는 업데이트된 아이템을 다시 마스터로 보내거나 직접 기록한다.  
이 방법은 마스터에서 데이터를 읽고 원격 워커에서 처리한 다음 다시 마스터에게 전송하므로, 네트워크 사용량이 매우 많아질 수 있다는 점에 유의해야 한다.  

 - `파티셔닝`

스프링 배치는 원격 파티셔닝 및 로컬 파티셔닝을 모두 지원한다.  
원겨 파티셔닝을 사용하면 내구성 있는 통신 방법이 필요하지 않으며 마스터는 워커의 스텝 수집을 위한 컨트롤러 역핢나 한다. 이 경우 각 워커의 스텝은 독립적으로 동작하며 로컬로 배포된 것처럼 동일하게 구성된다.  

<br/>

## 프로젝트 만들기

 - 프로젝트 구성
    - 사이트: https://start.spring.io
    - IDE(sts): https://spring.io/tools
    - IDE(IntelliJ): https://www.jetbrains.com/ko-kr/idea/download/?section=windows
```
Group ID: io.spring.batch
Artifact ID: hello-world
Build System: Maven
Language: Java 8+
Packaging: Jar
Version: 0.0.1-SNAPSHOT
Spring Boot Version: 2.3.7
Dependencies: Batch, H2, JDBC
```

 - HelloWorldApplication
    - @EnableBatchProcessing: 배치 인프라스트럭처를 부트스트랩하는 데 사용된다. 
        - JobRepository: 실행 중인 잡의 상태를 기록
        - JobLauncher: 잡을 구동
        - JobExplorer: JobRepository를 사용해 읽기 전용 작업을 수행
        - JobRegistry: 특정한 런처 구현체를 사용할 때 잡을 찾음
        - PlatformTransactionManager: 잡 진행 과정에서 트랜잭션을 다룸
        - JobBuilderFactory: 잡을 생성하는 빌더
        - StepBuilderFactory: 스텝을 생성하는 빌더
        - JobRepository와 PlatformTransactionManager는 필요에 따라 데이터 소스를 사용할 수 있다. 스프링 부트는 클래스 패스에 존재하는 HSQLDB를 사용해 이를 처리하는데, 스프링 배치 구동 시에 HSQLDB를 감지해 내장 데이터 소스를 생성한다.
     - @SpringBootApplication: @ComponentScan과 @EnableAutoConfiguration을 결합한 메타 애너테이션
        - 데이터 소스뿐만 아니라 스프링 부트 기반의 적절한 자동 구성을 만들어준다.
```Java
@EnableBatchProcessing
@SpringBootApplication
public class HelloWorldApplication {

	@Autowired
	private JobBuilderFactory jobBuilderFactory;

	@Autowired
	private StepBuilderFactory stepBuilderFactory;

	@Bean
	public Job job() {
		return this.jobBuilderFactory.get("job")
				.start(step())
				.build();
	}

	@Bean
	public Step step() {
		return this.stepBuilderFactory.get("step1")
				.tasklet(new Tasklet() {
					@Override
					public RepeatStatus execute(StepContribution contribution,
							ChunkContext chunkContext) {
						System.out.println("Hello, World!");
						return RepeatStatus.FINISHED;
					}
				}).build();
	}

	public static void main(String[] args) {
		SpringApplication.run(HelloWorldApplication.class, args);
	}
}
```

 - 잡 실행하기
    - 실제 동작으로는 JobLauncherCommandLineRunner라는 컴포넌트가 스프링 배치가 클래스 경로에 있다면 실행 시에 로딩되며, JobLauncher를 사용해 ApplicationContext에서 찾아낸 모든 잡을 실행한다.
    - 메인 메서드에서 스프링 부트를 부트스트랩할 때 ApplicationContext가 생성되고, JobLauncherCommandLineRunner가 실행됐으며 잡이 수행된다.
```
1.  컴파일을 하기 위해서 프로젝트의 최상위 경로에서 'mvn clean package' 명령을 실행한다.

2.  빌드가 완료되면 잡을 실행하는데, 기본적으로 스프링 부트는 구성된 ApplicationContext 내에서 찾은 모든 잡을 구동 시에 실행한다.
동작 방식을 변경할 필요가 있다면 프로퍼티를 사용해 다르게 구성할 수도 있다.

3. 빌드 완료시 target 디렉토리로 이동해 'java -jar hello-world-0.0.1-SNAPSHOT.jar'를 실행한다.
```
