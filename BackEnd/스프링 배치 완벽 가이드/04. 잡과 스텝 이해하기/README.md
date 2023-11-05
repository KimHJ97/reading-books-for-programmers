# 04장. 잡과 스텝 이해하기

## 잡(Job)

잡은 처음부터 끝까지 독립적으로 실행할 수 있는 고유하며 순서가 지정된 여러 스텝의 목록으로 정의할 수 있다.  
 - 유일하다
    - 스프링 배치 JOB은 코어 스프링 프레임워크를 사용한 빈 구성 방식과 동일하게 Java나 XML을 사용해 구성하며, 구성한 내용을 재사용할 수 있다.
    - 동일한 구성으로 필요한 만큼 잡을 실행할 수 있다.
 - 순서를 가진 여러 스텝의 목록이다
    - 모든 스텝을 논리적인 순서대로 실행할 수 있도록 잡을 구성한다.

<br/>


### 잡의 생명주기

잡의 실행은 잡 러너에서 시작된다.  
잡 러너는 잡 이름과 여러 파라미터를 받아들여 잡을 실행시키는 역할을 한다.  
스프링 배치는 CommandLineJobRunner, JobRegistryBackgroundJobRunner 2개의 잡 러너를 제공한다.  
 - CommandLineJobRunner: 스크립트를 이용하거나 명령행에서 직접 잡을 실행할 때 사용한다. CommandLineJobRunner는 스프링을 부트스트랩하고, 전달받은 파라미터를 사용해 요청된 잡을 실행한다.
 - JobRegistryBackgroundJobRunner: 스프링을 부트스트랩해서 기동한 자바 프로세스 내에서 쿼츠나 JMX 후크와 같은 스케줄러를 사용해 잡을 실행한다면, 스프링이 부트스트랩될 때 실행 가능한 잡을 가지고 있는 JobRegistry를 생성한다.

CommandLineRunner 구현체는 별도의 구성이 없다면 기본적으로 ApplicationContext에 정의된 Job 타입의 모든 빈을 기동 시에 실행한다.  

사용자가 스프링 배치를 실행할 때 잡 러너를 사용하긴 하지만, 잡 러너는 프레임워크가 제공하는 표준 모듈은 아니다. 실제로 프레임워크를 실행할 때 진입점은 잡 러너가 아닌 org.springframework.batch.core.launch.JobLauncher 인터페이스이다.  
CommandLineJobRunner와 JobLauncherCommandLineRunner 내부에서 사용하는 이 클래스는 요청된 잡을 실행할 때 코어 스프링의 TaskExecutor 인터페이스를 사용한다.  

배치 잡이 실행되면 JobInstance가 생성된다.  
JobInstance는 잡의 논리적 실행을 나타내며 잡 이름과 잡에 전달되는 파라미터 2가지 항목으로 식별된다.  
JobExecution은 잡 실행의 실제 시도를 의미한다.  
잡이 처음부터 끝까지 단번에 실행 완료됐다면 JobInstance와 JobExecution은 하나씩만 생성된다.  
첫 번째 잡 실행 후 오류 상태로 종료되어, 해당 JobInstance를 재실행하면 JobExecution은 하나 더 생성된다.

 - JobInstance
    - BATCH_JOB_INSTANCE: JobInstance 정보
    - BATCH_JOB_EXECUTION_PARAMS: JobInstance에 전달된 파라미터
 - JobExecution
    - BATCH_JOB_EXECUTION: JobExecution 정보
    - BATCH_JOB_EXECUTION_CONTEXT: JobExecution 실행 상태

<br/>

### 잡 구성하기

 - `application.properties`
    - MySQL 드라이버를 사용하는 데이터 소스를 생성한다.
    - 데이터베이스에 배치 스키마가 존재하지 않으며 자동으로 배치 스키마를 생성하도록 한다.
```properties
spring.datasource.driverClassName=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/spring_batch
spring.datasource.username=root
spring.datasource.password=p@ssw0rd
spring.batch.initialize-schema=always
# spring.datasource.schema=schema-mysql.sql
# spring.datasource.initialization-mode=always
# spring.batch.job.names=conditionalStepLogicJob
```

 - `HelloWorldJob`
```Java
@EnableBatchProcessing
@SpringBootApplication
public class HelloWorldJob {

	@Autowired
	private JobBuilderFactory jobBuilderFactory;

	@Autowired
	private StepBuilderFactory stepBuilderFactory;

	@Bean
	public Job job() {
		return this.jobBuilderFactory.get("basicJob")
				.start(step1())
				.build();
	}

	@Bean
	public Step step1() {
		return this.stepBuilderFactory.get("step1")
				.tasklet(helloWorldTasklet(null, null))
				.build();
	}
}
```

<br/>

## 스텝(Step)

스텝은 독립적이고 순차적으로 배치 처리를 수행한다.  
자체적으로 입력을 처리하고, 자체적인 처리기를 가질 수 있으며, 자체적으로 출력을 처리한다.  
트랜잭션은 스텝 내에서 이루어지며, 스텝은 서로 독립되도록 의도적으로 설계되었다.  

<br/>

### 태스크릿 처리와 청크 처리

태스크릿은 Tasklet 인터페이스를 사용해 Tasklet.execute 메서드가 RepeatStatus.FINISHED를 반환할 때까지 트랜잭션 범위 내에서 반복적으로 실행되는 코드 블록을 만들 수 있다.  
청크 기반 처리 모델은 최소한 2~3개의 주요 컴포넌트(ItemReader, ItemProcessor, ItemWriter)로 구성된다. 스프링 배치는 이러한 컴포넌트를 사용해 레코드를 청크 또는 레코드 그룹 단위로 처리한다. 각 청크는 자체 트랜잭션으로 실행되며, 처리에 실패했다면 마지막으로 성공한 트랜잭션 이후부터 다시 시작할 수 있다.  

ItemReader는 청크 단위로 처리할 모든 레코드를 반복적으로 메모리로 읽어온다.  
이후 메모리로 읽어들인 아이템은 반복적으로 ItemProcessor를 거쳐간다.  
마지막으로 한 번에 기록할 수 있는 ItemWriter를 호출하면서 모든 아이템을 전달한다.  
ItemWriter의 단일 호출은 물리적 쓰기를 일괄적으로 처리함으로써 IO 최적화를 이룬다.  

<div align="center">
	<img src="./images/chunk-oriented-processing-with-item-processor.png">
</div>

```Java
// 청크 기반 모델 의사코드
List items = new Arraylist();
for(int i = 0; i < commitInterval; i++){
    Object item = itemReader.read();
    if (item != null) {
        items.add(item);
    }
}

List processedItems = new Arraylist();
for(Object item: items){
    Object processedItem = itemProcessor.process(item);
    if (processedItem != null) {
        processedItems.add(processedItem);
    }
}

itemWriter.write(processedItems);
```

<br/>

### 스텝 구성하기

 - `태스크릿`
	- 태스크릿 스텝을 만드는 방법은 스프링 배치가 제공하는 MethodInvokingTaskletAdapter를 사용해서 사용자 코드를 태스크릿 스텝으로 정의하는 방법과 Tasklet 인터페이스를 구현하는 방법 2가지가 있다.
	- Tasklet 인터페이스는 execute 메서드를 구현하며, 처리 완료 이후에 스프링 배치가 어떤 일을 수행해야 할지 알 수 있도록 RepeatStatus 객체를 반환하면 된다.
		- RepeatStatus.CONTINUABLE: 해당 태스크릿을 다시 실행한다. 어떤 조건이 충족될 때까지 특정 태스크릿을 반복 실행해야 할 때 사용할 수 있다.
		- RepeatStatus.FINISHED: 성공 여부에 관계없이 태스크릿의 처리를 완료하고 다음 처리를 이어서 한다.
```Java
@EnableBatchProcessing
@Configuration
public class BatchConfiguration {

	@Autowired
	private JobBuilderFactory jobBuilderFactory;

	@Autowired
	private StepBuilderFactory stepBuilderFactory;

	@Bean
	public Job job() {
		return this.jobBuilderFactory.get("job")
									.start(step1())
									.build();
	}

	@Bean
	public Step step1() {
		return this.stepBuilderFactory.get("step1")
							.tasklet((stepContribution, chunkContext) -> {
								System.out.println("Hello, World!");
								return RepeatStatus.FINISHED;
							})
							.build();
	}
}
```

 - `청크 기반 스텝`
	- 청크는 커밋 간격에 의해 정의된다. 커밋 간격을 50개 아이템으로 설정했다면 잡은 50개 아이템을 읽고(Read), 50개 아이템을 처리(Process)한 다음에, 한 번에 50개 아이템을 기록(Write)한다.
	- 청크 사이즈를 10으로 지정한 경우 10개의 레코드를 읽고, 처리할 때까지 어떤 레코드도 쓰기 작업을 하지 않는다. 만약, 9개의 아이템을 처리한 후 오류가 발생하면 스프링 배치는 현재 청크(트랜잭션)를 롤백하고 잡이 실패했다고 표시한다.
```Java
@EnableBatchProcessing
@Configuration
public class BatchConfiguration {

	@Autowired
	private JobBuilderFactory jobBuilderFactory;

	@Autowired
	private StepBuilderFactory stepBuilderFactory;

	@Bean
	public Job job() {
		return this.jobBuilderFactory.get("job")
									.start(step1())
									.build();
	}

	@Bean
	public Step step1() {
		return this.stepBuilderFactory.get("step1")
							.<String, String>chunk(10)
							.reader(itemReader(null))
							.writer(itemWriter(null))
							.build();
	}

	@Bean
	@StepScope
	public FlatFileItemReader<String> itemReader(
			@Value("#{jobParameters['inputFile']}") Resource inputFile) {

		return new FlatFileItemReaderBuilder<String>()
						.name("itemReader")
						.resource(inputFile)
						.lineMapper(new PassThroughLineMapper())
						.build();
	}

	@Bean
	@StepScope
	public FlatFileItemWriter<String> itemWriter(
			@Value("#{jobParameters['outputFile']}") Resource outputFile) {

		return new FlatFileItemWriterBuilder<String>()
						.name("itemWriter")
						.resource(outputFile)
						.lineAggregator(new PassThroughLineAggregator<>())
						.build();
	}
}
```
