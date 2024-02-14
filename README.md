# 미니어처를 통한 생산환경 시뮬레이션을 위한 정보 관리 에이전트 개발
Database PLC Connection and Monitoring Agent
for research and developement project
                                                                                                       
## 프로잭트 개요
기존의 산업 시설의 시뮬레이션 환경에서 수작업으로 시뮬레이션 기기 간 통신하기 위해서는 많은 비용이 발생함.  
따라서, 시뮬레이션 기기 간 통신에 사용되는 프로토콜을 자동적으로 생성하는 기능을 모듈화하여 DLL 라이브러리를 제공하여, 시뮬레이션 과정의 비용을 최소화함.                                  
또한, 사용자 친화적인 인터페이스(Dashboard)를 제공하여 기기 간 통신 상황을 쉽게 파악하고 PLC 및 DB 수정을 용이하게 함.  

## 프로젝트 참여 인원
김대로 - PLC 통신 프로토콜 생성 함수 구현  
손원석 - Web Server 및 DB 구축   
박동욱 - .Net framwork를 통한 DLL포맷의 API 제작  
윤수빈 - DLL API 호출 함수 구현  
이해빈 - DLL API 호출 함수 구현  
최범규 - 대시보드 및 콜백 기능 구현  
김원아 - 대시보드 및 콜백 기능 구현  

## 구현 내용
### 1. Database와 PLC(Programmable Logic Controller)장치의 데이터송수신 API(.dll) 개발

![c1_c2](https://github.com/dhfgoeofh/DPCA/assets/80153046/9e99a229-3e0d-458a-9e65-b92dc810e698)

- PC-PLC 하드웨어간 연결방식에 따라 시리얼 통신과 이더넷 통신으로 구분됨.
- 따라서 시리얼/이더넷 통신을 지원하기 위해 각각에 방식에 대한 구현을 진행함.

![그림1](https://github.com/dhfgoeofh/DPCA/assets/80153046/4f0110c1-b512-4bc8-ba48-fb89fca696ee)

- 시리얼/이더넷 통신을 위한 프로토콜에 맞는 통신 명령어를 생성하도록 기능을 구현
- 기능 구현 사항은 다음과 같음
  1. PLC 통신 연결
  2. PLC 개별 읽기
  3. PLC 연속 읽기
  4. PLC 개별 쓰기
  5. PLC 연속 쓰기
  6. PLC 통신 종료

### 2. DLL API 제어를 위한 Local Web Server 개발

<img width="854" alt="시뮬레이션을 위한 정보 관리 에이전트 구조" src="https://github.com/dhfgoeofh/DPCA/assets/80153046/316607e4-bc8b-4501-b688-af74a2afebd8">

- Web Server(Flask)는 구현된 DLL API 함수를 호출하여 전체적인 PLC 통신을 제어함.

### 3. DB 구축 및 Server와 DB의 통신 기능 개발

![Web API](https://github.com/dhfgoeofh/DPCA/assets/80153046/c600a1ca-3dcf-466e-9606-6001965374ec)

- MySQL을 활용하여 DB를 구축  
- DB 데이터 읽기/쓰기를 위한 Execute 쿼리(GET, POST, PUT, DELETE) 기능을 구현함

### 3. DB 데이터 시각화와 PLC 및 DB 수정을 위한 대쉬보드 개발

![Reset클릭시DB,PLC쓰기_클릭강조](https://github.com/dhfgoeofh/DPCA/assets/80153046/9780a8e0-33b8-4d54-8473-9835502fd5c0)

- Dash API를 활용하여 로컬 인터페이스를 개발하였으며, 세부 콜백 기능을 추가하여 PLC와 DB의 데이터 수정을 가능하도록 함.

## 구현 계획  
1차 - 관련 자료 조사 (2023/11/24 - 2023/11/27)  
개발 관련 회의 - 2023/11/27  
2차 - API 기능 개발 (2023/11/27 - 2023/12/7)  
3차 - 보고서 작성 (2023/12/8 - 2023/12/28)  

