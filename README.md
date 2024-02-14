# 미니어처를 통한 생산환경 시뮬레이션을 위한 정보 관리 에이전트 개발
Database PLC Connection and Monitoring Agent
for research and developement project
                                                                                                       
## 프로잭트 개요
기존의 산업 시설의 시뮬레이션 환경에서 수작업으로 시뮬레이션 기기 간 통신하기 위해서는 많은 비용이 발생함.
따라서, 시뮬레이션 기기 간 통신에 사용되는 프로토콜을 자동적으로 생성하는 기능을 모듈화하여 DLL 라이브러리를 제공하여, 시뮬레이션 과정의 비용을 최소화함.                                
또한, 사용자 친화적인 인터페이스(Dashboard)를 제공하여 기기 간 통신 상황을 쉽게 파악하고 PLC 및 DB 수정을 용이하게 함.



## 목표 (우선순위)
1. Database와 PLC(Programmable Logic Controller)장치의 데이터송수신 API(.dll) DPCA 개발

<img width="854" alt="시뮬레이션을 위한 정보 관리 에이전트 구조" src="https://github.com/dhfgoeofh/DPCA/assets/80153046/316607e4-bc8b-4501-b688-af74a2afebd8">

2. DLL API는 Local Web Server를 통해 실행되며, DB와 PLC 간 데이터의 송수신을 기록을 출력하는 대쉬보드 구현

![Reset클릭시DB,PLC쓰기_클릭강조](https://github.com/dhfgoeofh/DPCA/assets/80153046/9780a8e0-33b8-4d54-8473-9835502fd5c0)




## 프로젝트 참여 인
김대로 - PLC 통신 프로토콜 생성 함수 구현
손원석 - Web Server 및 DB 구축 
박동욱 - .Net framwork를 통한 DLL포맷의 API 제작
윤수빈 - DLL API 호출 함수 구현
이해빈 - DLL API 호출 함수 구현
최범규 - 대시보드 및 콜백 기능 구현
김원아 - 대시보드 및 콜백 기능 구현

## 계획
1차 - 관련 자료 조사 (~11/24)
개발 관련 회의 - 11/27
2차 - API 기능 개발 (11/27~12/7, 2주 소요)
3차 - 보고서 작성 (12/8 ~ 12/28, 시험기간 2주이기 때문에 26~28일 마무리)
