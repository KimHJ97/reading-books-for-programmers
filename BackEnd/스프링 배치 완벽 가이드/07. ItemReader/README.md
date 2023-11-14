# 07장. ItemReader

스프링 배칭에서 청크 기반으로 동작하는 각 스텝은 ItemReader, ItemProcessor, ItemWriter로 구성된다.  
입력으로 제공될 수 있는 데이터의 유형은 플랫 파일, XML, 다양한 DB 등 여러 가지가 존재한다.  
스프링 배치는 개발자가 별도로 코드를 작성하지 않아도 다양한 유형의 입력 데이터를 처리할 수 있는 표준 방법을 제공하며, 웹 서비스로 데이터를 읽어들이는 것처럼 스프링 배치가 지원하지 않는 포맷의 데이터를 처리할 수 있는 커스텀 Reader를 개발하는 기능도 제공한다.  

<br/>

## ItemReader 인터페이스

ItemReader는 전략 인터페이스로 스프링 배치는 처리할 입력 유형에 맞는 여러 구현체(플랫 파일, DB, JMS 리소스, 기타 입력 등)를 제공한다.  
스프링 배치가 ItemReader의 read 메서드를 호출하면, 해당 메서드는 스텝 내에서 처리할 아이템 한 개를 반환한다.  
스텝에서는 아이템 개수를 세어서 청크 내의 데이터가 몇 개나 처리됐는지를 관리한다.  
해당 아이템은 구성된 특정 ItemProcessor로 전달되며 그 뒤 청크의 일부분에 포함돼 ItemWriter로 전달된다.  

 - ItemReader
```Java
package org.springframework.batch.item;

public interface ItemReader {
    T read() throws Exception, UnexpectedInputException, ParseException, NonTransientResourceException;
}
```

<br/>


