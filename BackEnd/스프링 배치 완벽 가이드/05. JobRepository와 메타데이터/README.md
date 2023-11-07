# 05장. JobRepository와 메타데이터

스프링 배치는 잡이 실행될 때 잡의 상태를 JobRepository에 저장해 관리한다.  
그리고 잡의 재시작 또는 아이템 재처리 시 어떤 동작을 수행할지 이 정보를 사용해 결정한다.  

<br/>

## JobRepository

스프링 배치는 기본적으로 관계형 데이터베이스에 배치 메타데이터를 저장한다.  
 - __BATCH_JOB_INSTANCE__ (JobInstance 저장)
    - 잡을 식별하는 고유 정보가 포함된 잡 파라미터로 잡을 처음 실행하면 단일 JobInstance 레코드가 테이블에 등록된다.
        - JOB_EXECUTION_ID: 테이블 기본 키
        - VERSION: 낙관적인 락에 사용되는 레코드 버전
        - JOB_NAME: 실행된 잡의 이름
        - JOB_KET: 잡 이름과 잡 파라미터의 해시 값, JobInstance를 고유하게 식별하는 데 사용되는 값
 - __BATCH_JOB_EXECUTION__ (JobExecution 저장)
    - 배치 잡의 실제 실행 기록을 나타낸다. 잡이 실행될 때마다 새 레코드가 해당 테이블에 생성되고, 잡이 진행되는 동안 주기적으로 업데이트된다.
        - JOB_EXECUTION_ID: 테이블 기본 키
        - VERSION: 낙관적인 락에 사용되는 레코드 버전
        - JOB_INSTANCE_ID: BATCH_JOB_INSTANCE 테이블을 참조하는 외래 키
        - CREATE_TIME: 레코드가 생성된 시간
        - START_TIME: 잡 실행이 시작된 시간
        - END_TIME: 잡 실행이 완료된 시간
        - STATUS: 잡 실행의 배치 상태
        - EXIT_CODE: 잡 실행의 종료 코드
        - EXIT_MESSAGE: EXIT_CODE와 관련된 메시지나 스택 트레이스
        - LAST_UPDATED: 레코드가 마지막으로 갱신된 시간
 - __BATCH_JOB_EXECUTION_CONTEXT__ (JobExecutionContext 저장)
    - 재시작같이 배치가 여러 번 실행되는 상황에서 ExecutionContext를 유용하게 사용하기 위해서는 스프링 배치가 관련 정보를 저장해야 한다. 해당 테이블은 JobExecution의 ExecutionContext를 저장하는 곳이다.
        - JOB_EXECUTION_ID: 테이블 기본 키
        - SHORT_CONTEXT: 트림 처리된 SERIALIZED_CONTEXT
        - SERIALIZED_CONTEXT: 직렬화된 ExecutionContext
 - __BATCH_JOB_EXECUTION_PARAMS__ (Job Parameters 저장)
    - 해당 테이블은 잡이 매번 실행될 때마다 사용된 잡 파라미터를 저장한다. 재시작시에는 잡의 식별 정보 파라미터만 자동으로 전달된다.
        - JOB_EXECUTION_ID: 테이블 기본 키
        - TYPE_CODE: 파라미터 값의 타입을 나타내는 문자열
        - KEY_NAME: 파라미터 이름
        - STRING_VAL: 타입이 String인 경우 파라미터 값
        - DATE_VAL: 타입이 Date인 경우 파라미터 값
        - LONG_VAL: 타입이 Long인 경우 파라미터 값
        - DOUBLE_VAL: 타입이 Double인 경우 파라미터 값
        - IDENTIFYING: 파라미터가 식별되는지 여부를 나타내는 플래그
 - __BATCH_STEP_EXECUTION__
    - 스텝의 시작, 완료, 상태에 대한 메타데이터를 저장한다. 또한, 스텝 분석이 가능하도록 다양한 횟수 값을 추가로 저장한다. 읽기 횟수, 처리 횟수, 쓰기 횟수, 건너뛰기 횟수 등과 같은 모든 데이터가 저장된다.
        - STEP_EXECUTION_ID: 테이블 기본 키
        - VERSION: 낙관적인 락에 사용되는 레코드 버전
        - STEP_NAME: 스텝 이름
        - JOB_EXECUTION_ID: BATCH_JOB_EXECUTION 테이블을 참조하는 외래 키
        - START_TIME: 스텝 실행이 시작된 시간
        - END_TIME: 스텝 실행이 완료된 시간
        - STATUS: 스텝의 배치 상태
        - COMMIT_COUNT: 스텝 실행 중에 커밋된 트랜잭션 수
        - READ_COUNT: 읽은 아이템 수
        - FILTER_COUNT: 아이템 프로세서가 null을 반환해 필터링된 아이템 수
        - WRITE_COUNT: 기록된 아이템 수
        - READ_SKIP_COUNT: ItemReader 내에서 예외가 던져졌을 때 건너뛴 아이템 수
        - PROCESS_SKIP_COUNT: ItemProcessor 내에서 예외가 던져졌을 때 건너뛴 아이템 수
        - WRITE_SKIP_COUNT: ItemWriter 내에서 예외가 던져졌을 때 건너뛴 아이템 수
        - ROLLBACK_COUNT: 스텝 실행에서 롤백된 트랜잭션 수
        - EXIT_CODE: 스텝의 종료 코드
        - EXIT_MESSAGE: 스텝 실행에서 반환된 메시지나 스택 트레이스
        - LAST_UPDATED: 레코드가 마지막으로 업데이트된 시간
 - __BATCH_STEP_EXECUTION_CONTEXT__
    - 컴포넌트의 상태 저장에 사용되는 ExecutionContext가 JobExecution 내에 존재하는 것처럼, StepExecution에도 동일한 목적으로 사용되는 ExecutionContext가 존재한다. StepExecution의 ExecutionContext는 스텝 수준에서 컴포넌트의 상태를 저장하는 데 사용된다.
        - STEP_EXECUTION_ID: 테이블 기본 키
        - SHORT_CONTEXT: 트림 처리된 SERIALIZED_CONTEXT
        - SERIALIZED_CONTEXT: 직렬화된 ExecutionContext

<br/>

### 인메모리 JobRepository

스프링 배치는 개발이나 테스트 환경에서 사용할 수 있는 인모메리 JobRepository 방식을 제공한다.  
기본적으로 java.util.Map 객체를 데이터 저장소로 사용하는 JobRepository 구현체를 제공한다.  

<br/>

### BatchConfigurer 인터페이스

BatchConfigurer 인터페이스는 스프링 배치 인프라스트럭처 컴포넌트의 구성을 커스터마이징하는 데 사용되는 전략 인터페이스이다.  
@EnableBatchProcessing 어노테이션을 적용하면 스프링 배치는 BatchConfigurer 인터페이스를 사용해 프레임워크에서 사용되는 각 인프라스트럭처 컴포넌트의 인스턴스를 얻는다.  
BatchConfigurer 구현체에서 빈을 생성하고, SimpleBatchConfiguration에서 스프링의 ApplicationContext에 생성한 빈을 등록한다.  

스프링 배치 인프라스트럭처의 주요 컴포넌트로는 JobRepository, JobLauncher, PlatformTransactionManager, JobExplorer 등이 있다.  
대부분 이 모든 인터페이스를 직접 구현할 필요는 없고, 스프링 배치가 제공하는 DefaultBatchConfigurer를 사용하면 모든 기본 옵션이 제공된다.  
때문에, BatchConfigurer 구현체를 새로 만들기보다는 DefaultBatchConfigurer를 상속해 적절한 메서드를 재정의하는 방식으로 쉽게 사용 가능하다.  

```Java
public interface BatchConfigurer {
    JobRepository getJobRepository() throws Exception;
    PlatformTransactionManager getTransactionManager() throws Exception;
    JobLauncher getJobLauncher() throws Exception;
    JobExplorer getJobExplorer() throws Exception;
}
```

<br/>

### JobRepository 커스터마이징하기

JobRepository는 JobRepositoryFactoryBean이라는 FactoryBean을 통해 생성된다.  

 - `JobRepositoryFactoryBean 커스터마이징 옵션`
```
setClobType: CLOB 컬럼에 사용할 타입을 나타내는 java.sql.Type 값을 받는다.
setSerializer: JobExecution의 ExecutionContext 및 StepExecutionContext의 ExecutionContext를 직렬화하고 역직렬화하는 데 사용할 ExecutionContextSerializer 구현체 구성에 사용한다.
setLobHandler: 실제로 LOB를 특별하게 취급해야 하는 Oracle의 예전 버전을 사용할 때 필요한 설정이다.
setMaxVarCharLength: 짧은 실행 컨텍스트 컬럼뿐만 아니라 종료 메시지의 길이를 자르는 데 사용한다. 스프링 배치에서 제공하는 스키마를 수정하지 않는 한 설정해서는 안 된다.
setDataSource: JobRepository와 함께 사용할 데이터 소스를 설정한다.
setJdbcOperations: JdbcOperations 인스턴스를 지정하는 수정자. 지정하지 않으면 setDataSource 메서드에 지정한 데이터 소스를 사용해 새 JdbcOperations 객체를 생성한다.
setDatabaseType: 데이터베이스 유형을 설정한다. 스프링 배치는 데이터베이스 유형을 자동으로 식별하려고 시도하므로 일반적으로 설정할 필요가 없다.
setTablePrefix: 모든 테이블의 이름에 기본적으로 사용되는 "BATCH_" 라는 접두어 이외의 다른 접두어를 지정할 때 사용한다.
setIncrementerFactory: 대부분의 테이블의 기본 키를 증분하는 데 사용되는 증분기 팩토리를 지정한다.
setValidateTransactionState: JobExecution이 생성될 대 기존 트랜잭션이 있는지 여부를 나타내는 플래그다. 이런 경우는 일반적으로 실수이기 때문에 기본값은 true이다.
setIsolationLevelForCreate: JobExecution 엔티티가 생성될 때 사용되는 트랜잭션 직렬화 수준을 지정한다. 기본값은 ISOLATION_SERIALIZABLE이다.
setTransactionManager: 복수 개의 데이터베이스를 사용할 때는 두 데이터베이스를 동기화할 수 있도록 2단계 커밋을 지원하는 TransactionManager를 지정한다.
```

 - `JobRepository 커스터 마이징`
```Java
public class CustomBatchConfigurer extends DefaultBatchConfigurer {

    @Autowired
    @Qualifier("repositoryDataSource")
    private DataSource dataSource;

    @Override
    protected JobRepository createJobRepository() throws Exception {
        JobRepositoryFactoryBean factoryBean = new JobRepositoryFactoryBean();
        factoryBean.setDatabaseType(DatabaseType.MYSQL.getProductName());
        factoryBean.setTablePrefix("FOO_");
        factoryBean.setIsolationLevelForCreate("ISOLATION_REPEATABLE_READ");
        factoryBean.setDataSource(this.dataSource);
        factoryBean.afterPropertiesSet();
        return factoryBean.getObject();
    }
}
```

 - `TransactionManager 커스터 마이징`
    - getTransactionManager() 메서드를 호출하면 배치 처리에 사용할 목적으로 어딘가에 정의해둔 PlatformTransactionManager가 명시적으로 반환된다.
    - TransactionManager가 생성되지 않은 경우에는 DefaultBatchConfigurer가 기본적으로 setDataSource 수정자 내에서 DataSourceTransactionManager를 자동으로 생성한다.
```Java
public class CustomBatchConfigurer extends DefaultBatchConfigurer {

    @Autowired
    @Qualifier("batchTransactionManager")
    private PlatformTransactionManager transactionManager;

    @Override
    protected PlatformTransactionManager getTransactionManager() {
        return this.transactionManager;
    }
}
```

 - `JobExplorer 커스터 마이징`
    - JobRepository는 배치 잡의 상태를 저장하는 데이터 저장소에 데이터를 저장하고 조회할 수 있도록 API를 제공한다.
    - 때로는, 배치 잡의 상태 데이터를 읽기 전용으로만 볼 수 있도록 제공하고 싶은 경우가 있다. 이러한 경우 JobExplorer를 이용하여 배치 메타데이터를 읽기 전용으로 제공할 수 있다.
```Java
public class CustomBatchConfigurer extends DefaultBatchConfigurer {

    @Autowired
    @Qualifier("batchTransactionManager")
    private DataSource dataSource;

    @Override
    protected JobExplorer createJobExplorer() throws Exception {
        JobExplorerFactoryBean factoryBean = new JobExplorerFactoryBean();

        factoryBean.setDataSource(this.dataSource);
        factoryBean.setTablePrefix("FOO_");

        factoryBean.afterPropertiesSet();

        return factoryBean.getObject();
    }
}
```

 - `JobLauncher 커스터 마이징`
    - JobLauncher는 스프링 배치 잡을 실행하는 진입점이다. 스프링 부트는 기본적으로 스프링 배치가 제공하는 SimpleJobLauncher를 사용한다.
    - setJobRepository: 사용할 JobRepository 지정
    - setTaskExecutor: JobLauncher에 사용할 TaskExecutor 설정. 기본적으로 SyncTaskExecutor가 설정된다.

<br/>

### 데이터베이스 구성하기

스프링 부트 및 배치에서 사용할 데이터베이스를 구성하기 위해서는 데이터베이스 드라이버를 클래스 경로에 추가하고 적절한 프로퍼티를 구성하기만 하면 된다.  

 - application.yml
    - spring.batch.initialize-schema: 스프링 부트가 스프링 배치 스키마 스크립트를 실행하도록 설정한다.
        - always: 애플리케이션을 실행할 대마다 스크립트가 실행된다. 스프링 배치 SQL 파일에 drop문이 ㅇ벗고 오류가 발생하면 무시되므로, 개발 환경일 떄 사용하기 좋다.
        - never: 스크립트를 실행하지 않는다.
        - embedded: 내장 데이터베이스를 사용할 때, 각 실행 시마다 데이터가 초기화된 데이터베이스 인스턴스를 사용한다는 가정으로 스크립트를 실행한다.
```YML
spring:
  datasource:
    driverClassName: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/spring_batch
    username: 'root'
    password: 'p@ssw0rd'
  batch:
    initialize-schema: always
```

<br/>

### 잡 메타데이터 사용하기

스프링 배치가 제공하는 메타데이터 접근하기 위해서 사용되는 방법으로는 JobExplorer를 사용할 수 있다.  
JobExplorer 인터페이스는 JobRepository에 있는 이력 데이터나 최신 데이터에 접근하는 시작점이다.  
배치 프레임워크 컴포넌트가 JobRepository를 사용해 잡 실행과 관련해 저장된 정보에 접근하지만, JobExplorer는 데이터베이스에 직접 접근한다.  
JobExplorer의 기본적인 목적은 읽기 전용으로 JobRepository의 데이터에 접근하는 기능을 제공하는 것이다.  
JobInstance 및 JobExecution과 관련된 정보를 얻을 수 있는 메서드를 제공한다.  

JobExplorer를 사용해 RunIdIncrementer내에서 run.id 파라미터 값을 찾을 수 있고,  
새 인스턴스를 시작하기 전에 잡이 현재 실행 중인지 확인하는 데 사용할 수 있다.  

```
findRunningjobExecutions: 종료 시간이 존재하지 않는 모든 JobExecution을 반환
findJobInstanceByName: 전달받은 이름을 가진 JobInstance 목록을 반환 (페이징 처리된 목록)
getJobExecution: 전달받은 ID를 가진 JobExecution 반환, 존재하지 않으면 null 반환
getJobExecutions: 전달받은 JobInstance와 관련된 모든 JobExecution 목록 반환
getJobInstance: 전달받은 ID를 가진 JobInstance 반환, 존재하지 않으면 null 반환
getJobInstances: 전달받은 인덱스부터 지정한 개수만큼의 범위 내에 있는 JobInstance 반환
getJobInstanceCount: 전달받은 잡 이름으로 생성된 JobInstance 개수 반환
getJobNames: JobRepository에 저장돼 있는 고유한 모든 잡 이름을 알파뱃 순서대로 반환
getStepExecution: 전달받은 StepExecution의 ID와 부모 JobInstance의 ID를 가진 StepExecution 반환
```

 - DemoApplication
    - JobExplorer가 어떻게 동작하는지 확인하기 위해 Tasklet에 주입한 후 조작
```Java
@EnableBatchProcessing
@SpringBootApplication
public class DemoApplication {

	@Autowired
	private JobBuilderFactory jobBuilderFactory;

	@Autowired
	private StepBuilderFactory stepBuilderFactory;

	@Autowired
	private JobExplorer jobExplorer;

	@Bean
	public Job explorerJob() {
		return this.jobBuilderFactory.get("explorerJob")
				.start(explorerStep())
				.build();
	}

	@Bean
	public Step explorerStep() {
		return this.stepBuilderFactory.get("explorerStep")
				.tasklet(explorerTasklet())
				.build();
	}

	@Bean
	public Tasklet explorerTasklet() {
		return new ExploringTasklet(this.jobExplorer);
	}

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

}
```

 - ExploringTasklet
    - ExploringTasklet 실행시 JobExplorer를 주입받고, JobExplorer의 getJobInstances() 메서드로 JobInstance의 정보 얻기
    - 아래 예제는 JobInstance가 얼마나 많이 실행됐는지, 각 JobInstance당 얼마나 많은 실제 실행이 있었고 그 결과가 어땠는지를 출력한다.
```Java
public class ExploringTasklet implements Tasklet {

	private JobExplorer explorer;

	public ExploringTasklet(JobExplorer explorer) {
		this.explorer = explorer;
	}

	public RepeatStatus execute(StepContribution stepContribution, ChunkContext chunkContext) {

		String jobName = chunkContext.getStepContext().getJobName();

		List<JobInstance> instances =
				explorer.getJobInstances(jobName,
						0,
						Integer.MAX_VALUE);

		System.out.println(
				String.format("There are %d job instances for the job %s",
				instances.size(),
				jobName));

		System.out.println("They have had the following results");
		System.out.println("************************************");

		for (JobInstance instance : instances) {
			List<JobExecution> jobExecutions = this.explorer.getJobExecutions(instance);

			System.out.println(
					String.format("Instance %d had %d executions",
							instance.getInstanceId(),
							jobExecutions.size()));

			for (JobExecution jobExecution : jobExecutions) {
				System.out.println(
						String.format("\tExecution %d resulted in Exit Status %s",
								jobExecution.getId(),
								jobExecution.getExitStatus()));
			}
		}

		return RepeatStatus.FINISHED;
	}
}
```
