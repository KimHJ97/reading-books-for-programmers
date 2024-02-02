# Real MySQL 8.0 1

## 책 소개

 - 제목: Real MySQL 8.0 1
    - 부제: 개발자와 DBA를 위한 MySQL 실전 가이드
 - 지은이: 백은빈, 이성욱
 - 펴낸이: 박찬규
 - 펴낸곳: 위키북스
 - 초판 1쇄 발행: 2021년 12월 10일

<br/>

## 책 정보

 - 도서 홈페이지: https://wikibook.co.kr/realmysql801
 - 깃허브 저장소: https://github.com/wikibook/realmysql80

<br/>

## 예제 데이터베이스

 - `예제 데이터베이스 생성`
    - https://github.com/wikibook/realmysql80
    - 예제 데이터베이스 생성 후 깃허브 저장소의 employees.sql 쿼리를 적용한다.
```sql
CREATE DATABASE employees
    DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE employees
SOURCE employees.sql
```

<br/>

## 목차

 - CHAPTER 01 소개
 - CHAPTER 02 설치와 설정
 - CHAPTER 03 사용자 및 권한
 - CHAPTER 04 아키텍처
 - CHAPTER 05 트랜잭션과 잠금
 - CHAPTER 06 데이터 압축
 - CHAPTER 07 데이터 암호화
 - CHAPTER 08 인덱스
 - CHAPTER 09 옵티마이저와 힌트
 - CHAPTER 10 실행 계획

