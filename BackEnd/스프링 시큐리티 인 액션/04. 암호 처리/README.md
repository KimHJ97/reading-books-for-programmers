# 4장. 암호 처리

 - `인코딩, 암호화 해싱`
    - 인코딩(Encoding): 주어진 입력에 대한 모든 변환을 의미한다.
    - 암호화(Encryption): 출력을 얻기 위해 입력 값과 키를 모두 지정하는 특정한 유형의 인코딩이다. 키를 이용하면 나중에 누가 출력에서 입력을 얻는 함수를 호출할 수 있는지 선택할 수 있다.
        - 대칭키 암호화: 암호화에 쓰는 키와 복호화에 쓰는 키가 같다.
        - 비대칭 키 암호화: 암호화와 복호화에 쓰는 키가 서로 다르다.
    - 해싱: 함수가 한 방향으로만 작동하는 특정한 유형의 인코딩이다.
 - `스프링 시큐리티 주요 인터페이스`
    - UserDetails: 스프링 시큐리티가 관리하는 사용자
    - GrantedAuthority: 애플리케이션의 목적 내에서 사용자에게 허용되는 작업 정의(읽기, 쓰기, 삭제 등)
    - UserDetailsService: 사용자 이름으로 사용자 세부 정보를 검색하는 객체
    - UserDetailsManager: UserDetailsService의 더 구체적인 계약으로 사용자 이름으로 사용자를 검색하는 것 외에도 사용자 컬렉션이나 특정 사용자를 변경할 수도 있다.
    - PasswordEncoder: 암호를 암호화 또는 해시하는 방법과 주어진 인코딩된 문자열을 일반 텍스트 암호와 비교하는 방법을 지정한다.

<br/>

## PasswordEncoder

일반적으로 시스템은 암호를 일반 텍스트로 관리하지 않고 공격자가 암호를 읽고 훔치기 어렵게 하기 위한 일종의 변환 과정을 거친다.  
PasswordEncoder는 인증 프로세스에서 암호가 유효한지를 확인한다. 모든 시스템은 어떤 방식으로든 인코딩된 암호를 저장하며 아무도 암호를 읽을 수 없게 해시를 저장하는 것이 좋다.  

 - PasswordEncoder 인터페이스
    - encode() 메서드는 주어진 문자열을 변환해 반환한다. 스프링 시큐리티 기능의 관점에서 이 메서드는 주어진 암호의 해시를 제공하거나 암호화를 수행하는 일을 한다.
    - matches() 메서드는 지정된 암호를 인증 프로세스에서 알려진자격 증명의 집합을 대상으로 비교한다.
    - upgradeEncoding() 메서드는 기본값 false를 반환한다. true를 반환하도록 메서드를 재정의하면 인코딩된 암호를 보안 향상을 위해 다시 인코딩한다.
```Java
public interface PasswordEncoder {

    String encode(CharSequence rawPassword);
    boolean matches(CharSequence rawPassword, String encodePassword);

    default boolean upgradeEncoding(String encodedPassword) {
        return false;
    }
}
```

<br/>

### PasswordEncoder 구현

 - PlainTextPasswordEncoder
    - 암호를 인코딩하지 않고 일반 텍스트로 간주한다.
```Java
public class PlainTextPasswordEncoder implements PasswordEncoder {

    @Override
    String encode(CharSequence rawPassword) {
        return rawPassword.toString();
    }

    @Override
    boolean matches(CharSequence rawPassword, String encodePassword) {
        return rawPassword.equals(encodedPassword);
    }
}
```

 - Sha512PasswordEncoder
```Java
public class Sha512PasswordEncoder implements PasswordEncoder {

    @Override
    String encode(CharSequence rawPassword) {
        return hashWithSHA512(rawPassword.toString());
    }

    @Override
    boolean matches(CharSequence rawPassword, String encodePassword) {
        String hashedPassword = encode(rawPassword);
        return encodedPassword.equals(hashedPassword);
    }

    // SHA-512 해시 메서드 구현
    private String hashWithSHA512(String input) {
        StringBuilder result = new StringBuilder();
        try {
            MessageDigest md = MessageDigest.getInstance("SHA-512");
            byte[] digested = md.digest(input.getBytes());
            for (int i = 0; i < digested.length; i++) {
                result.append(Integer.toHexString(0xFF & digested[i]));
            }
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("Bad algorithm");
        }
        return result.toString();
    }
}
```

<br/>

### PasswordEncoder 제공된 구현 선택

스프링 시큐리티에 이미 유용한 PasswordEncoder 구현체가 제공된다.
 - NoOpPasswordEncoder: 암호를 인코딩하지 않고 일반 텍스트로 유지한다.
 - StandardPasswordEncoder: SHA-256을 이용해 암호를 해시한다.
 - Pbkdf2PasswordEncoder: PBKDF2를 이용해 암호를 해시한다.
 - BCryptPasswordEncoder: bcrypt 강력 해싱 함수로 암호를 인코딩한다.
 - SCryptPasswordEncoder: scrypt 해싱 함수로 암호를 인코딩한다.

<br/>

#### `PasswordEncoder 구현 인스턴스 만들기`

 - PBKDF2는 반복 횟수 인수만큼 HMAC를 수행하는 아주 단순하고 느린 해싱 함수다. 해시가 길수록 암호가 강력해지지만, 성능에 영향을 주고, 반복 횟수로 애플리케이션 소비 리소스가 증가한다.
```Java
// NoOpPasswordEncoder
PasswordEncoder passwordEncoder = NoOpPasswordEncoder.getInstance();

// SHA-256 Encoder
PasswordEncoder passwordEncoder = new StandardPasswordEncoder();
PasswordEncoder passwordEncoder = new StandardPasswordEncoder("비밀키");

// Pbkdf2 Encoder
PasswordEncoder passwordEncoder = new Pbkdf2PasswordEncoder();
PasswordEncoder passwordEncoder = new Pbkdf2PasswordEncoder("비밀키");
PasswordEncoder passwordEncoder = new Pbkdf2PasswordEncoder("비밀키", 185000, 256); // 키, 반복횟수, 해시 크기

// BCrypt Encoder
PasswordEncoder passwordEncoder = new BCryptPasswordEncoder();
PasswordEncoder passwordEncoder = new BCryptPasswordEncoder(4);

SecureRandom secureRandom = SecureRandom.getInstanceStrong();
PasswordEncoder passwordEncoder = new BCryptPasswordEncoder(4, secureRandom);

// Scrypt Encoder
PasswordEncoder passwordEncoder = new SCryptPasswordEncoder();
PassowrdEncoder passwordEncoder = new SCryptPasswordEncoder(16384, 8, 1, 32, 64); // CPU비용, 메모리비용, 병렬화계수, 키길이, 솔트길이
```

<br/>

#### `DelegatingPasswordEncoder를 이용한 여러 인코딩 전략`

DelegatingPasswordEncoder는 PasswordEncoder 인터페이스의 한 구현이며 자체 인코딩 알고리즘을 구현하는 대신 같은 계약의 다른 구현 인스턴스에 작업을 위임한다. 해시는 해당 해시를 의미하는 알고리즘의 이름을 나타내는 접두사로 시작한다.  
 - NoOpPasswordEncoder: {noop}
 - BCryptPasswordEncoder: {bcrypt}
 - SCryptPasswordEncoder: {scrypt}
```Java
@Configuration
public class ProjectConfig {

    ..

    @Bean
    public PasswordEncoder passwordEncoder() {
        Map<String, PasswordEncoder> encoders = new HashMap<>();

        encoders.put("noop", NoOpPasswordEncoder.getInstance());
        encoders.put("bcrypt", new BCryptPasswordEncoder());
        encoders.put("scrypt", new SCryptPasswordEncoder());

        return new DelegatingPasswordEncoder("bcrypt", encoders);
    }
}
```

<br/>

## 스프링 시큐리티 암호화 모듈에 관한 추가 정보

 - 키 생성기: 해싱 및 암호화 알고리즘을 위한 키를 생성하는 객체
 - 암호기: 데이터를 암호화 및 복호화하는 객체

### 키 생성기

키 생성기는 특정한 종류의 키를 생성하는 객체로서 일반적으로 암호화나 해싱 알고리즘에 필요하다.  
BytesKeyGenerator 및 StringKeyGenerator는 키 생성기의 두 가지 주요 유형을 나타내는 인터페이스이며 팩토리 클래스 KeyGenerator로 직접 만들 수 있다.  
StringKeyGenerator 계약으로 나타내는 문자열 키 생성기를 이용해 문자열 키를 얻을 수 있다. 일반적으로 이 키는 해싱 또는 암호화 알고리즘의 솔트 값으로 이용된다.  

 - StringKeyGenerator 인터페이스
    - 8바이트 키를 생성하고 이를 16진수 문자열로 인코딩한다.
```Java
public interface StringKeyGenerator {
    String generateKey();
}

// 사용 예시
StringKeyGenerator keyGenerator = KeyGenerators.string();
String salt = keyGenerator.generateKey();
```

 - BytesKeyGenerator 인터페이스
    - byte[] 키를 반환하는 generateKey() 메서드와 키 길이(Byte 수)를 반환하는 메서드가 있다.
    - 기본적으로 8바이트 길이의 키를 생성하고, 다른 키 길이를 지정하려면 키 생성기 인스턴스를 얻을 때 값을 입력한다.
```Java
public interface BytesKeyGenerator {
    int getKeyLength();
    byte[] generateKey();
}

// 사용 예시
BytesKeyGenerator keyGenerator = KeyGenerators.secureRandom();
// BytesKeyGenerator keyGenerator = KeyGenerators.secureRandom(16);
byte[] key = keyGenerator.generateKey();
int keyLength = keyGenerator.getKeyLength();

// secureRandom()으로 생성한 BytesKeyGenerator는 generateKey()를 호출할 대마다 고유한 키를 생성한다.
// 같은 키 생성자를 호출하면 같은 키를 반환하는 구현이 적합한 경우가 있다.
BytesKeyGenerator keyGenerator = KeyGenerators.shared(16);
byte[] key1 = keyGenerator.generateKey();
byte[] key2 = keyGenerator.generateKey();
```

<br/>

### 암호기

암호기를 암호화 알고리즘을 구현하는 객체이다.  
암호기는 암호화와 복호화 작업을 지원하며 SSCM에는 이를 위해 BytesEncryptor 및 TextEncryptor라는 두 유형이 암호기를 제공한다.  

 - TextEncryptor 인터페이스
```Java
public interface TextEncryptor {
    String encrypt(String text);
    String decrypt(String encryptedText);
}
```

 - BytesEncryptor 인터페이스
```Java
public interface BytesEncryptor {
    byte[] encrypt(byte[] byteArray);
    byte[] decrypt(byte[] encryptedByteArray);
}
```

 - 암호기 이용 예시
    - 내부적으로 표준 바이트 암호기는 256 바이트 AES 암호화를 이용해 입력을 암호화한다. (CBC 암호 블록 체인 방식)
    - 더 강력한 바이트 암호기 인스턴스를 만들려면 Encryptors.stronger() 메서드를 호출하면 된다. (GCM 갈루아/카운터 모드)
```Java
String salt = KeyGenerators.string().generateKey();
String password = "secret";
String valueToEncrypt = "Hello";

BytesEncryptor encryptor = Encryptors.standard(password, salt);
byte[] encrypted = encryptor.encrypt(valueToEncrypt.getBytes());
byte[] decrypted = encryptor.decrypt(encrypted);
```

 - TextEncryptors
    - TextEncryptors는 세 가지 주요 형식이 있으며 Encryptors.text(), Encryptors.delux(), Encryptors.queryableText() 메서드를 호출해 이러한 형식을 생성할 수 있다.
    - Encryptors.text(), Encryptors.delux()는 같은 입력으로 encrypt() 메서드를 반복 호출해도 다른 출력이 반환된다. 그 이유는 암호화 프로세스에 임의의 초기화 벡터가 생성되기 떄문이다. 만약, 입력이 같을 때 같은 출력 생성하도록 보장하길 원한다면 Encryptors.queryableText()를 이용한다.
```Java
// 암호화하지 않는 TextEncryptor
// 암호화에 시간을 소비하지 않고 애플리케이션 성능을 테스트할 때 이용할 수 있다.
String valueToEncrypt = "Hello";
TextEncryptor encryptor = Encryptors.noOpText();
String encrypted = encryptor.encrypt(valueToEncrypt);

// 초기화 벡터를 이용하는 TextEncryptor
String salt = KeyGenerators.string().generateKey();
String password = "secret";
String valueToEncrypt = "Hello";

TextEncryptor encryptor = Encryptors.text(password, salt);
String encrypted = encryptor.encrypt(valueToEncrypt);
String decrypted = encryptor.decrypt(encrypted);
```
