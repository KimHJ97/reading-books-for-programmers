# 근접성 서비스

근접성 서비스는 음식점, 호텔, 극장, 박물관 등 현재 위치에서 가까운 시설을 찾는 데 이용된다.  

## 1. 문제 이해 및 설계 범위 확정

 - 사용자가 검색 반경을 지정할 수 있는가?
    - 검색 반경 내에 표시할 사업장이 충분치 않은 경우 검색 반경 시스템이 알아서 넓혀야 하는가?
        - 주어진 반경 내의 사업장만 대상
        - 시간이 남은 경우 주어진 범위 안에서 사업장이 많지 않은 경우 어떻게 처리할 것인지 고려
 - 검색 반경 변경은 어떻게 하는가?
    - 0.5km, 1km, 2km, 5km, 20km 등 선택지가 주어진다.
 - 사업장 정보는 어떻게 관리되는가?
    - 변경된 사업장 정보는 실시간으로 보여져야 하는가?
        - 사업장 소유주가 사업장 정보를 추가, 삭제, 갱신할 수 있다.
        - 갱신한 정보는 다음날까지 반영되어야 한다. (계약서에 명시)
 - 사용자 이동 중 검색 결과 갱신해야 하는가?
    - 사용자의 이동은 고려하지 않는다. (갱신할 필요 없음)

<br/>

### 1-1. 기능 요구사항

 - 사용자의 위치와 검색 반경 정보에 매치되는 사업장 목록 반환
 - 사업장 소유주가 사업장 정보를 추가, 삭제, 갱신할 수 있도록 하되, 그 정보가 검색 결과에 실시간으로 반영될 필요는 없음
 - 고객은 사업장의 상세 정보를 살필 수 있음

<br/>

### 1-2. 비기능 요구사항

 - 낮은 응답 지연(latency): 사용자는 주변 사업장을 신속히 검색할 수 있어야 한다.
 - 데이터 보호(data privacy): 사용자 위치는 민감 정보다. 위치 기반 서비스를 설계할 떄는 언제나 사용자의 정보를 보호할 방법을 고려해야 한다.
 - 고가용성(high availability) 및 규모 확장성 요구사항: 인구 밀집 지역에서 이용자가 집중되는 시간에 트래픽이 급증해도 감당할 수 있도록 시스템을 설계해야 한다.

<br/>

## 2. 개략적 설계안 제시 및 동의 구하기

 - API 설계
 - 개략적 설계안
 - 주변 사업장 검색 알고리즘
 - 데이터 모델

<br/>

### 2-1. API 설계

 - 사업장 목록 검색 
    - HTTP Method: GET
    - URL: /v1/search/nearby
```
Request
latitude: 검색할 위도
longitude: 검색할 경도
radius(optional): 생략할 경우 기본값은 5000m

Response
{
    "total": 10,
    "businesses": [
        {business object},
        {business object},
        ..
    ]
}
```

<br/>

 - 사업장 관련 API
    - 사업장 상세 정보 조회: GET /v1/businesses/:id
    - 새로운 사업장 추가: POST /v1/businesses
    - 사업장 상세 정보 변경: PUT /v1/businesses/:id
    - 사업장 정보 삭제: DELETE v1/businesses/:id

<br/>

### 2-2. 데이터 모델

 - __읽기/쓰기 비율__

읽기 연산은 주변 사업장 검색, 사업장 정보 확인 등 굉장히 자주 수행된다.  
쓰기 연산은 사업장 정보 추가, 삭제, 수정 등 실행 빈도가 낮다.  

<br/>

 - __데이터 스키마__

business 테이블은 사업장 상세 정보는 담는다.

```
business_id
address
city
state
country
latitude
longtitude
```

<br/>

### 2-3. 계략적 설계

 - __로드밸런서__
    - 로드밸런서는 유입 트래픽을 자동으로 여러 서비스에 분산시키는 컴포넌트다. 통상적으로 로드밸런서를 사용하는 회사는 로드밸런서에 단일 DNS 진입점을 지정하고, URL 경로를 분석하여 어느 서비스에 트래픽을 전달할 지 결정한다.  

<br/>

 - __위치 기반 서비스(LBS)__
    - LBS는 시스템의 핵심 부분으로, 주어진 위치와 반경 정보를 이용해 주변 사업장을 검색한다.
    - 쓰기 요청이 없는, 일기 요청만 빈번하게 발생하는 서비스이다.
    - QPS가 높다. 특히 특정 시간대의 인구 밀집 지역일수록 그 경향이 심하다.
    - 무상태 서비스이므로 수평적 규모 확장이 쉽다.

<br/>

 - __사업장 서비스__
    - 사업장 소유주가 사업장 정보를 생성, 갱신, 삭제한다. 기본적으로 쓰기 요청이며, QPS는 높지 않다.
    - 고객이 사업장 정보를 조회한다. 특정 시간대에 QPS가 높아진다.

<br/>

 - __데이터베이스 클러스터__
    - 데이터베이스 클러스터는 주 부(primary-secondary) 데이터베이스 형태로 구성할 수 있다.
    - 주 데이터베이스는 쓰기 요청을 처리하며, 부 데이터베이스(사본 데이터베이스)는 읽기 요청을 처리한다.
    - 데이터는 일단 주 데이터베이스에 기록된 다음에 사본 데이터베이스로 복사된다.
        - 복제에 걸리는 시간 지연 떄문에 주 데이터베이스 데이터와 사본 데이터베이스 데이터 사이에는 차이가 있을 수 있다.

<br/>

 - __사업장 서비스와 LBS의 규모 확장성__
    - 사업장 서비스와 LBS는 둘 다 무상태 서비스로 점심시간 등의 특정 시간 대에 집중적으로 몰리는 트래픽에는 자동으로 서버를 추가하여 대응하고, 야간 등 유휴 시간 대에는 서버를 삭제하도록 구성할 수 있다.
    - 시스템 클라우드에 둔다면 여러 지역, 여러 가용성 구역에 서버를 두어 시스템 가용성을 높일 수 있다.

<br/>

### 2-4. 주변 사업장 검색 알고리즘

많은 회사에서 레디스 지오해시(Geohash in Redis)나 PostGIS 확장을 설치한 포스트그레스(Postgres) 데이터베이스를 활용한다.  
데이터베이스의 이름을 나열하기 보다는 지리적 위치 색인이 어떻게 동작하는지 설명함으로써 문제 풀이 능력과 기술적 지식을 갖추는 것이 좋다.  

<br/>










