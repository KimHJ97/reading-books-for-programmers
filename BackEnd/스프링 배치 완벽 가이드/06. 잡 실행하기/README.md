# 06장. 잡 실행하기

## 스프링 부트로 배치 잡 시작하기

스프링 부트는 CommandLineRunner와 ApplicationRunner라는 두 가지 메커니즘을 이용해 실행 시 로직을 수행한다.  
스프링 부트를 스프링 배치와 함께 사용할 때는 JobLauncherCommandLineRunner라는 특별한 CommandLineRunner가 사용된다.  

JobLauncherCommandLineRunner는 스프링 배치의 JobLauncher를 사용해 잡을 실행한다.  
스프링 부트가 ApplicationContext 내에 구성된 모든 CommandLineRunner를 실행할 대, 클래스패스에 spring-boot-starter-batch가 존재한다면 JobLauncherCommandLineRunner는 컨텍스트 내에서 찾아낸 모든 잡을 실행한다.  
스프링 부트 속성으로 spring.batch.job.enabled를 false로 설정하면 애플리케이션 기동시 자동으로 잡이 실행되는 것을 없앨 수 있다.  

 - 애플리케이션 기동 시 잡이 실행되지 않게 구성하기
```Java
@EnableBatchProcessing
@SpringBootApplication
public class NoRunJob {

    @Autowired
    private JobBuilderFactory jobBuilderFacotry;

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
                        System.out.println("Step1 run!");
                        return RepeatStatus.FINISHED;
                    })
                    .build();
    }

    public static void main(String[] args) {
        SpringApplication application = new SpringApplication(NoRunJob.class);

        Properties properties = new Properties();
        properties.put("spring.batch.job.enabled", false);
        application.setDefaultProperties(properties);

        application.run(args);
    }
}
```

<br/>

### REST 방식으로 잡 실행하기

JobLauncher 인터페이스는 잡을 실행시키는 인터페이스이다.  
JobLauncher 인터페이스에는 run 메서드 하나만 존재하며, 실행할 잡 및 잡에 전달할 잡 파라미터를 매개변수로 전달받는다.

 - JobLauncher
```Java
public interface JobLauncher {
    public JobExecution run(Job job, JobParameters jobParameters) throws 
                                JobExecutionAlreadyRunningException,
                                JobRestartException,
                                JobInstanceAlreadyCompleteException,
                                JobParametersInvalidException;
}
```

<br/>

스프링 배치는 JobLauncher 구현체인 SimpleJobLauncher를 제공한다.  
SimpleJobLauncher는 잡 실행과 관련된 대부분의 요구 사항을 만족한다.  
잡의 실행이 기존 잡 인스턴스의 일부인지 새로운 잡의 일부인지를 판별해 그에 맞는 동작을 한다.  

기본적으로 SimpleJobLauncher는 동기식 TaskExecutor를 사용해 잡을 동기식으로 실행한다.  
만약, 다른 쓰레드에서 잡을 실행하려면 비동기식 TaskExecutor 구현체를 선택해야 한다.  

 - pom.xml
    - Batch, MySQL, JDBC, Web 의존성을 추가한다.
```XML
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-batch</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-jdbc</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>mysql</groupId>
        <artifactId>mysql-connector-java</artifactId>
        <scope>runtime</scope>
    </dependency>
```

 - application.yml
```YML
spring:
  batch:
    job:
      enabled: false
      initialize-schema: always
  datasource:
    driverClassName: com.mysql.cj.jdbc.Driver
    url: jdbc:mysql://localhost:3306/spring_batch
    username: 'root'
    password: 'p@ssw0rd'
    platform: mysql
```

 - RestApplication
```Java
@EnableBatchProcessing
@SpringBootApplication
public class RestApplication {

	@Autowired
	private JobBuilderFactory jobBuilderFactory;

	@Autowired
	private StepBuilderFactory stepBuilderFactory;

    // Job 정의
	@Bean
	public Job job() {
		return this.jobBuilderFactory.get("job")
				.incrementer(new RunIdIncrementer())
				.start(step1())
				.build();
	}

    // Step 정의
	@Bean
	public Step step1() {
		return this.stepBuilderFactory.get("step1")
				.tasklet((stepContribution, chunkContext) -> {
					System.out.println("step 1 ran today!");
					return RepeatStatus.FINISHED;
				}).build();
	}

    // Controller 정의 (엔드포인트)
	@RestController
	public static class JobLaunchingController {

		@Autowired
		private JobLauncher jobLauncher;

		@Autowired
		private ApplicationContext context;

		@Autowired
		private JobExplorer jobExplorer;

		@PostMapping(path = "/run")
		public ExitStatus runJob(@RequestBody JobLaunchRequest request) throws Exception {
			Job job = this.context.getBean(request.getName(), Job.class);

			return this.jobLauncher.run(job, request.getJobParameters()).getExitStatus();
		}
	}

    // Job 파라미터 DTO 정의
	public static class JobLaunchRequest {
		private String name;

		private Properties jobParameters;

		// Getter & Setter
        ..

		public JobParameters getJobParameters() {
			Properties properties = new Properties();
			properties.putAll(this.jobParameters);

			return new JobParametersBuilder(properties)
					.toJobParameters();
		}
	}

	public static void main(String[] args) {
		new SpringApplication(RestApplication.class).run(args);
	}
}
```

 - `잡 실행 전에 잡 파라미터 증가시키기`
    - JobParametersIncrementer를 사용할 떄 파라미터의 변경 사항을 적용하는 일은 JobLauncher가 수행한다.
    - 스프링 배치는 JobParametersBuilder의 getNextJobParameters 메서드처럼 파라미터를 증가시키는 편리한 메서드를 제공한다.
        - JobParametersBuilder.getNextJobParameters(job) 메서드를 호출하면 run.id라는 파라미터가 추가된 새로운 JobParameters 인스턴스가 생성된다.
        - getNextJobParameters 메서드는 Job이 JobParametersIncrementer를 가지고 있는지 해당 Job을 보고서 판별하고, JobParametersIncrementer를 가지고 있다면 마지막 JobExecution에 사용됐던 JobParameters에 적용한다.
        - 또한, 이 실행이 재시작인지 여부를 판별하고 JobParameters를 적절하게 처리한다.
```Java
@EnableBatchProcessing
@SpringBootApplication
public class RestApplication {

    // @Autowired
    ..

    // Job & Step 정의
    ..

	@RestController
	public static class JobLaunchingController {

		@Autowired
		private JobLauncher jobLauncher;

		@Autowired
		private ApplicationContext context;

		@Autowired
		private JobExplorer jobExplorer;

		@PostMapping(path = "/run")
		public ExitStatus runJob(@RequestBody JobLaunchRequest request) throws Exception {
			Job job = this.context.getBean(request.getName(), Job.class);

			JobParameters jobParameters =
					new JobParametersBuilder(request.getJobParameters(),
								this.jobExplorer)
							.getNextJobParameters(job)
							.toJobParameters();

			return this.jobLauncher.run(job, jobParameters).getExitStatus();
		}
	}
}
```

<br/>

## 쿼츠를 사용해 스케줄링하기

쿼츠는 오픈소스 스케줄러 라이브러리로 스케줄러, 잡, 트리거 라는 세 가지 주요 컴포넌트를 가지고 있다.  
스케줄러는 SchedulerFactory를 통해서 가져올 수 있으며 JobDetails 및 트리거의 저장소 기능을 한다.  
또한, 스케줄러는 연관된 트리거가 작동할 때 잡을 실행하는 역할을 하며, 잡은 실행할 작업의 단위이다.  
트리거는 작업 실행 시점을 정의한다. 트리거가 작동돼 쿼츠에게 잡을 실행하도록 지시하면 잡의 개별 실행을 정의하는 JobDetails 객체가 생성된다.  

<br/>

 - pom.xml
    - Batch, MySQL, JDBC, Quartz sCHEDULER 의존성을 추가한다.
```XML
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-quartz</artifactId>
    </dependency>
    ..
```

 - `잡 스케줄링`
    - QuartzJobBean 클래스를 상속받고, executeInternal 메서드를 재정의한다. 해당 메서드는 스케줄링된 이벤트가 발생할 때마다 한 번씩 호출된다.
    - 스케줄링을 구성하기 위해서는 JobBuilder를 사용해 쿼츠 잡의 빈을 구성한다.
    - 다음으로 SimpleScheduleBuilder를 사용해 스케줄링의 주기를 구성한다.
    - 다음으로 TriggerBuilder를 사용해 scheduleBuilder의 스케줄링 주기와 JobBuilder로 등록한 쿼츠 잡 정보로 트리거할 수 있다.
```Java
// QuartzJobConfiguration: 배치 Job 정의
@EnableBatchProcessing
@SpringBootApplication
public class QuartzJobConfiguration {

	@Configuration
	public class BatchConfiguration {

		@Autowired
		private JobBuilderFactory jobBuilderFactory;

		@Autowired
		private StepBuilderFactory stepBuilderFactory;

		@Bean
		public Job job() {
			return this.jobBuilderFactory.get("job")
					.incrementer(new RunIdIncrementer())
					.start(step1())
					.build();
		}

		@Bean
		public Step step1() {
			return this.stepBuilderFactory.get("step1")
					.tasklet((stepContribution, chunkContext) -> {
						System.out.println("step1 ran!");
						return RepeatStatus.FINISHED;
					}).build();
		}
	}

	public static void main(String[] args) {
		SpringApplication.run(QuartzJobConfiguration.class, args);
	}
}

// BatchScheduledJob: 쿼츠 Job 정의
public class BatchScheduledJob extends QuartzJobBean {

	@Autowired
	private Job job;

	@Autowired
	private JobExplorer jobExplorer;

	@Autowired
	private JobLauncher jobLauncher;

	@Override
	protected void executeInternal(JobExecutionContext context) {
		JobParameters jobParameters = new JobParametersBuilder(this.jobExplorer)
				.getNextJobParameters(this.job)
				.toJobParameters();

		try {
			this.jobLauncher.run(this.job, jobParameters);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}

// QuartzConfiguration: 쿼츠 스케줄링 정의
@Configuration
public class QuartzConfiguration {

	@Bean
	public JobDetail quartzJobDetail() {
		return JobBuilder.newJob(BatchScheduledJob.class)
				.storeDurably()
				.build();
	}

	@Bean
	public Trigger jobTrigger() {
        // 5초마다 한 번씩 잡을 기동하며, 최초 한 번 수행 이후 4번 반복
		SimpleScheduleBuilder scheduleBuilder = SimpleScheduleBuilder.simpleSchedule()
				.withIntervalInSeconds(5).withRepeatCount(4);

		return TriggerBuilder.newTrigger()
				.forJob(quartzJobDetail())
				.withSchedule(scheduleBuilder)
				.build();
	}
}
```

<br/>

## 잡 중지하기

잡이 이상적으로 자연스럽게 끝나기를 원하지만 실행 도중에 멈춰야 하는 경우도 있다.  
특정한 이유로 인해 처리 중인 잡 실행을 프로그래밍적으로 중지할 수 있으며, 외부에서 잡을 중지시킬 수도 있다.  

<br/>

## 중지 트랜지션 사용하기

 - 시나리오
    - 단순한 거래 파일을 불러온다. 각 거래는 계좌번호, 타임스탬프, 금액으로 구성된다. 파일 내용은 파일 내 총 레코드 개수를 보여주는 한 줄짜리 요약 레코드로 끝난다.
    - 거래 정보를 거래 테이블에 저장한 이후에 계좌번호와 현재 계좌 잔액으로 구성된 별도의 계좌 요약 테이블에 적용한다.
    - 각 계좌의 계좌번호와 잔액을 나열하는 요약 파일을 생성한다.

<br/>

 - transaction.csv 및 summary.csv 파일 예시
```
Transaction File:
3985729387,2010-01-08 12:15:26,523.65
3985729387,2010-01-08 1:28:58,-25.93
2

Summary File:
3985729387,497.72
```

 - schema-mysql.sql
```SQL
CREATE  TABLE IF NOT EXISTS account_summary (
  id INT NOT NULL AUTO_INCREMENT ,
  account_number VARCHAR(10) NOT NULL ,
  current_balance DECIMAL(10,2) NOT NULL ,
  PRIMARY KEY (id) )
ENGINE = InnoDB;

CREATE  TABLE IF NOT EXISTS transaction (
  id INT NOT NULL AUTO_INCREMENT ,
  timestamp TIMESTAMP NOT NULL ,
  amount DECIMAL(8,2) NOT NULL ,
  account_summary_id INT NOT NULL ,
  PRIMARY KEY (id) ,
  INDEX fk_Transaction_Account_Summary (account_summary_id ASC) ,
  CONSTRAINT fk_Transaction_Account_Summary
    FOREIGN KEY (account_summary_id )
    REFERENCES Account_Summary (id )
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;
```

 - 도메인 객체
    - Transaction, AccountSummary
```Java
@Getter
@Setter
public class Transaction {

	private String accountNumber;
	private Date timestamp;
	private double amount;
}

@Getter
@Setter
public class AccountSummary {

	private int id;
	private String accountNumber;
	private Double currentBalance;
}
```

 - `TransactionReader`
    - read(): 해당 리더에게 주입된 위임 리더에게 실제 읽기 작업을 위임한다. (FlatFileItemReader에게 동작 위임)
    - process(): FieldSet을 전달받아 어떤 유형의 레코드인지 판단한다.
```Java
public class TransactionReader implements ItemStreamReader<Transaction> {

	private ItemStreamReader<FieldSet> fieldSetReader;
	private int recordCount = 0;
	private int expectedRecordCount = 0;

	private StepExecution stepExecution;

	public TransactionReader(ItemStreamReader<FieldSet> fieldSetReader) {
		this.fieldSetReader = fieldSetReader;
	}

	public Transaction read() throws Exception {
		return process(fieldSetReader.read());
	}

	private Transaction process(FieldSet fieldSet) {
		Transaction result = null;

		if(fieldSet != null) {
			if(fieldSet.getFieldCount() > 1) {
                // 레코드가 두 개 이상이면 데이터 레코드
				result = new Transaction();
				result.setAccountNumber(fieldSet.readString(0));
				result.setTimestamp(fieldSet.readDate(1, "yyyy-MM-DD HH:mm:ss"));
				result.setAmount(fieldSet.readDouble(2));

				recordCount++;
			} else {
                // 그 외 푸터 레코드
				expectedRecordCount = fieldSet.readInt(0);

				if(expectedRecordCount != this.recordCount) {
					this.stepExecution.setTerminateOnly();
				}
			}
		}

		return result;
	}

	public void setFieldSetReader(ItemStreamReader<FieldSet> fieldSetReader) {
		this.fieldSetReader = fieldSetReader;
	}

	@AfterStep
	public ExitStatus afterStep(StepExecution execution) {
		if(recordCount == expectedRecordCount) {
			return execution.getExitStatus();
		} else {
			return ExitStatus.STOPPED;
		}
	}

	@BeforeStep
	public void beforeStep(StepExecution execution) {
		this.stepExecution = execution;
	}

	@Override
	public void open(ExecutionContext executionContext) throws ItemStreamException {
		this.fieldSetReader.open(executionContext);
	}

	@Override
	public void update(ExecutionContext executionContext) throws ItemStreamException {
		this.fieldSetReader.update(executionContext);
	}

	@Override
	public void close() throws ItemStreamException {
		this.fieldSetReader.close();
	}
}
```

 - `TransactionDao`
    - 제공된 계좌번호와 연관된 거래 목록을 반환한다.
```Java
// TransactionDao 인터페이스
public interface TransactionDao {

	List<Transaction> getTransactionsByAccountNumber(String accountNumber);
}

// TransactionDaoSupport
public class TransactionDaoSupport extends JdbcTemplate implements TransactionDao {

	public TransactionDaoSupport(DataSource dataSource) {
		super(dataSource);
	}

	@SuppressWarnings("unchecked")
	public List<Transaction> getTransactionsByAccountNumber(String accountNumber) {
		return query(
				"select t.id, t.timestamp, t.amount " +
						"from transaction t inner join account_summary a on " +
						"a.id = t.account_summary_id " +
						"where a.account_number = ?",
				new Object[] { accountNumber },
				(rs, rowNum) -> {
					Transaction trans = new Transaction();
					trans.setAmount(rs.getDouble("amount"));
					trans.setTimestamp(rs.getDate("timestamp"));
					return trans;
				}
		);
	}
}
```

 - `TransactionApplierProcessor`
    - 전달받은 각 AccountSummary 레코드를 기반으로 TransactionDao를 사용해 모든 거래 정보를 조회하며, 거래 정보에 따라 계좌의 현재 잔액을 증가하거나 감소시킨다.
```Java
public class TransactionApplierProcessor implements ItemProcessor<AccountSummary, AccountSummary> {

	private TransactionDao transactionDao;

	public TransactionApplierProcessor(TransactionDao transactionDao) {
		this.transactionDao = transactionDao;
	}

	public AccountSummary process(AccountSummary summary) throws Exception {
		List<Transaction> transactions = transactionDao
				.getTransactionsByAccountNumber(summary.getAccountNumber());

		for (Transaction transaction : transactions) {
			summary.setCurrentBalance(summary.getCurrentBalance()
					+ transaction.getAmount());
		}
		return summary;
	}
}
```

 - `TransactionProcessingJob`
    - TransactionFileStep을 등록한다.
```Java
@EnableBatchProcessing
@SpringBootApplication
public class TransactionProcessingJob {

	@Autowired
	private JobBuilderFactory jobBuilderFactory;

	@Autowired
	private StepBuilderFactory stepBuilderFactory;

    // ItemReader 정의
	@Bean
	@StepScope
	public TransactionReader transactionReader() {
		return new TransactionReader(fileItemReader(null));
	}

	@Bean
	@StepScope
	public FlatFileItemReader<FieldSet> fileItemReader(
			@Value("#{jobParameters['transactionFile']}") Resource inputFile) {
		return new FlatFileItemReaderBuilder<FieldSet>()
				.name("fileItemReader")
				.resource(inputFile)
				.lineTokenizer(new DelimitedLineTokenizer())
				.fieldSetMapper(new PassThroughFieldSetMapper())
				.build();
	}

    // ItemWriter 정의
	@Bean
	public JdbcBatchItemWriter<Transaction> transactionWriter(DataSource dataSource) {
		return new JdbcBatchItemWriterBuilder<Transaction>()
				.itemSqlParameterSourceProvider(
						new BeanPropertyItemSqlParameterSourceProvider<>())
				.sql("INSERT INTO TRANSACTION " +
						"(ACCOUNT_SUMMARY_ID, TIMESTAMP, AMOUNT) " +
						"VALUES ((SELECT ID FROM ACCOUNT_SUMMARY " +
						"	WHERE ACCOUNT_NUMBER = :accountNumber), " +
						":timestamp, :amount)")
				.dataSource(dataSource)
				.build();
	}

    // Step 정의(Reader + Writer)
	@Bean
	public Step importTransactionFileStep() {
		return this.stepBuilderFactory.get("importTransactionFileStep")
				.<Transaction, Transaction>chunk(100)
				.reader(transactionReader())
				.writer(transactionWriter(null))
				.allowStartIfComplete(true)
				.listener(transactionReader())
				.build();
	}
}
```

 - `TransactionProcessingJob`
    - ApplyTransactionStep을 등록한다.
    - 파일에서 찾은 거래 정보를 계좌에 적용한다.
```Java
@EnableBatchProcessing
@SpringBootApplication
public class TransactionProcessingJob {

    ..

    // ItemReader 정의
	@Bean
	@StepScope
	public JdbcCursorItemReader<AccountSummary> accountSummaryReader(DataSource dataSource) {
		return new JdbcCursorItemReaderBuilder<AccountSummary>()
				.name("accountSummaryReader")
				.dataSource(dataSource)
				.sql("SELECT ACCOUNT_NUMBER, CURRENT_BALANCE " +
						"FROM ACCOUNT_SUMMARY A " +
						"WHERE A.ID IN (" +
						"	SELECT DISTINCT T.ACCOUNT_SUMMARY_ID " +
						"	FROM TRANSACTION T) " +
						"ORDER BY A.ACCOUNT_NUMBER")
				.rowMapper((resultSet, rowNumber) -> {
					AccountSummary summary = new AccountSummary();

					summary.setAccountNumber(resultSet.getString("account_number"));
					summary.setCurrentBalance(resultSet.getDouble("current_balance"));

					return summary;
				}).build();
	}

	@Bean
	public TransactionDao transactionDao(DataSource dataSource) {
		return new TransactionDaoSupport(dataSource);
	}

    // ItemProcessor 정의
	@Bean
	public TransactionApplierProcessor transactionApplierProcessor() {
		return new TransactionApplierProcessor(transactionDao(null));
	}

    // ItemWriter 정의
	@Bean
	public JdbcBatchItemWriter<AccountSummary> accountSummaryWriter(DataSource dataSource) {
		return new JdbcBatchItemWriterBuilder<AccountSummary>()
				.dataSource(dataSource)
				.itemSqlParameterSourceProvider(
						new BeanPropertyItemSqlParameterSourceProvider<>())
				.sql("UPDATE ACCOUNT_SUMMARY " +
						"SET CURRENT_BALANCE = :currentBalance " +
						"WHERE ACCOUNT_NUMBER = :accountNumber")
				.build();
	}

    // Step 정의(Reader + Processor + Writer)
	@Bean
	public Step applyTransactionsStep() {
		return this.stepBuilderFactory.get("applyTransactionsStep")
				.<AccountSummary, AccountSummary>chunk(100)
				.reader(accountSummaryReader(null))
				.processor(transactionApplierProcessor())
				.writer(accountSummaryWriter(null))
				.build();
	}

}
```

 - `TransactionProcessingJob`
    - GenerateAccountSummaryStep 등록한다.
    - 계좌번호와 현재 잔액으로 CSV 파일을 생성한다.
```Java
@EnableBatchProcessing
@SpringBootApplication
public class TransactionProcessingJob {

    ..

    // ItemReader 정의
	@Bean
	@StepScope
	public JdbcCursorItemReader<AccountSummary> accountSummaryReader(DataSource dataSource) {
		return new JdbcCursorItemReaderBuilder<AccountSummary>()
				.name("accountSummaryReader")
				.dataSource(dataSource)
				.sql("SELECT ACCOUNT_NUMBER, CURRENT_BALANCE " +
						"FROM ACCOUNT_SUMMARY A " +
						"WHERE A.ID IN (" +
						"	SELECT DISTINCT T.ACCOUNT_SUMMARY_ID " +
						"	FROM TRANSACTION T) " +
						"ORDER BY A.ACCOUNT_NUMBER")
				.rowMapper((resultSet, rowNumber) -> {
					AccountSummary summary = new AccountSummary();

					summary.setAccountNumber(resultSet.getString("account_number"));
					summary.setCurrentBalance(resultSet.getDouble("current_balance"));

					return summary;
				}).build();
	}

    // ItemWriter 정의
	@Bean
	@StepScope
	public FlatFileItemWriter<AccountSummary> accountSummaryFileWriter(
			@Value("#{jobParameters['summaryFile']}") Resource summaryFile) {

		DelimitedLineAggregator<AccountSummary> lineAggregator = new DelimitedLineAggregator<>();
		BeanWrapperFieldExtractor<AccountSummary> fieldExtractor = new BeanWrapperFieldExtractor<>();
		fieldExtractor.setNames(new String[] {"accountNumber", "currentBalance"});
		fieldExtractor.afterPropertiesSet();
		lineAggregator.setFieldExtractor(fieldExtractor);

		return new FlatFileItemWriterBuilder<AccountSummary>()
				.name("accountSummaryFileWriter")
				.resource(summaryFile)
				.lineAggregator(lineAggregator)
				.build();
	}

    // Step 정의(Reader + Writer)
	@Bean
	public Step generateAccountSummaryStep() {
		return this.stepBuilderFactory.get("generateAccountSummaryStep")
				.<AccountSummary, AccountSummary>chunk(100)
				.reader(accountSummaryReader(null))
				.writer(accountSummaryFileWriter(null))
				.build();
	}

}
```

 - `Job 구성`
    - 스프링 배치 플로우를 이용해 start(), on(), from() 으로 흐름을 제어할 수 있다.
    - stepExecution.setTerminateOnly() 메서드로 스텝이 완료된 후 스프링 배치가 종료되도록 할 수 있다.
```Java
	@Bean
	public Job transactionJob() {
		return this.jobBuilderFactory.get("transactionJob")
				.start(importTransactionFileStep())
				.next(applyTransactionsStep())
				.next(generateAccountSummaryStep())
				.build();
//		return this.jobBuilderFactory.get("transactionJob")
//				.start(importTransactionFileStep())
//				.on("STOPPED").stopAndRestart(importTransactionFileStep())
//				.from(importTransactionFileStep()).on("*").to(applyTransactionsStep())
//				.from(applyTransactionsStep()).next(generateAccountSummaryStep())
//				.end()
//				.build();
	}

	public static void main(String[] args) {
		List<String> realArgs = new ArrayList<>(Arrays.asList(args));

		realArgs.add("transactionFile=input/transactionFile.csv");
		realArgs.add("summaryFile=file:///Users/mminella/tmp/summaryFile3.csv");

		SpringApplication.run(TransactionProcessingJob.class, realArgs.toArray(new String[realArgs.size()]));
	}
```

<br/>

### 오류 처리

스프링 배치는 잡이 중지되면 현재 청크를 롤백하며, 성공적으로 완료한 작업만 커밋하게 된다. 또한, 재시작 시에는 중단됐던 부분을 찾아낼 수 있다.  
스프링 배치는 예외가 발생하면 기본적으로 스텝 및 잡이 실패한 것으로 간주한다.  
스프링 배치의 기본적인 예외 처리 방식은 실패 상태로 잡을 중지하는 것이지만 다른 옵션도 있다.  

 - `TransactionReader 예외 던지도록 수정`
    - 25개의 레코드를 읽은 후 ParseException 예외를 발생시킨다.
    - 예외가 발생하면 스프링 배치는 스텝과 잡이 실패한 것으로 여기고, 잡 처리가 중지된다.
```Java
	private Transaction process(FieldSet fieldSet) {
		if(this.recordCount == 25) {
			throw new ParseException("This isn't what I hoped to happen");
		}

		Transaction result = null;

		..

		return result;
	}
```

<br/>

### 재시작 제어하기

스프링 배치는 예외가 발생하면 ExitStatus.FAILD 상태가 된다.  
스텝이 FAILD 상태로 식별되면 스프링 배치는 해당 스텝을 처음부터 다시 시작하지는 않는다.  
예외가 발생할 때 어떤 청크를 처리 중이었는지 기억하고, 잡을 재시작하면 중단됐던 부분을 가져온다.  
예를 들어, 어떤 잡의 10개의 청크 중에 2번째 청크가 처리 중이며 각 청크는 5개의 아이템으로 구성된다고 가정했을 때 2번쨰 청크의 4번쨰 아이템 처리시 예외가 발생하였다면, 현재 청크의 1~4번째 아이템 처리는 롤백되며, 재시작하면 스프링 배치는 청크 1을 건너뛴다.  

 - `잡의 재시작 방지하기`
    - JobBuilder의 preventRestart() 메서드를 호출하면, 잡이 실패하거나 어떤 이유로든 중지된 경우 다시 실행할 수 없게 한다.
```Java
	@Bean
	public Job transactionJob() {
		return this.jobBuilderFactory.get("transactionJob")
				.preventRestart()
				.start(importTransactionFileStep())
				.next(applyTransactionsStep())
				.next(generateAccountSummaryStep())
				.build();
    }
```

<br/>

 - `재시작 횟수 제한하도록 구성하기`
    - 만약에, 잡의 스텝 중 하나가 어떤 웹사이트에서 파일을 다운로드 하던 중에 해당 사이트의 네트워크 문제로 인해 실패했다고 가정한다면 10분 후에 다시 시도하면 정상적으로 동작될 수도 있다.
    - 하지만, 다운로드를 무한정 시도하고 싶지 않은 경우에 특정 횟수만큼만 시도하게 구현해야할 필요가 있다.
    - 스프링 배치는 이러한 기능을 잡 대신 스텝 수준으로 제공한다.
```Java
	@Bean
	public Step importTransactionFileStep() {
		return this.stepBuilderFactory.get("importTransactionFileStep")
                .startLimit(2)
				.<Transaction, Transaction>chunk(100)
				.reader(transactionReader())
				.writer(transactionWriter(null))
				.allowStartIfComplete(true)
				.listener(transactionReader())
				.build();
	}
```

 - `완료된 스텝 재실행하기`
    - 스프링 배치를 사용하면 동일한 파라미터로 잡을 한 번만 성공적으로 실행할 수 있다.
    - 그러나, 스텝에서는 이 규칙을 적용하지 않고 여러번 실행하도록 설정할 수 있다.
```Java
	@Bean
	public Step importTransactionFileStep() {
		return this.stepBuilderFactory.get("importTransactionFileStep")
                .allowStartIfComplete(true)
				.<Transaction, Transaction>chunk(100)
				.reader(transactionReader())
				.writer(transactionWriter(null))
				.allowStartIfComplete(true)
				.listener(transactionReader())
				.build();
	}
```
