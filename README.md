# 창의학기제_장고프로젝트

------
### 주요기능

   	1. 게시판 모듈화
   	2. 문서공유
   	3. 파일공유/클라우드
   	4. 채팅
   	5. 게시판 익명기능
   	6. 채팅로그를 기반으로 가산점 부과
------
### 개발상황

      1. 웹 사이트 기본기능
       - 기본 로그인, 로그아웃, 회원가입 기능 구현 (MySQL과 연동 완료)
       - 전체적인 웹 페이지 템플릿 구조 구현 및 디자인 템플릿 적용
       - 세부적인 사이트 맵 구상과 세부 디자인 수정 필요

   	2. 게시판 모듈화
       - '강의별 게시판' 항목 계정별로 글쓰기
       - 게시물 들어가서 수정 및 삭제 가능


   	3. 문서공유(04/04)
       - FireBase의 Firepad API를 이용한 문서공유 시스템 구현중
       - 웹 사이트 접속시 기본적인 문서공유는 되나 같은 그룹 회원끼리의 문서공유는 아직 안돼서 구현중
       - 그룹(과제) 테이블을 만들어서 문서공유 관련 정보를 DB에 저장할 계획
       - 장고에서 기본적으로 제공해주는 로그인 시스템 auth_user 테이블을 프록시 방식으로 확장해서 사용할 계획

   	4. 파일 공유/클라우드
         6주차 4/8 ~ 4/12

       * 진행중
          

       * 계획
          - 알림 추가 기능 -> 안 읽은 알림이 있으면 알려주도록 ui 및 추가 연동 계획.


       * 완료된 사항
          - 알고리즘 코드 모두 삭제.
          - 파일 delete 버튼 추가 및 연동 그리고 버그수정 완료.
          - 파일 업로드는 과목을 선택한 후에 가능하도록 하였음.
          - 파일 리스트 그룹화,알림 기능 그룹별 연동 진행할 계획, 사용자가 속한 그룹 정보 볼 수 있도록 수정 등 진행중..
          - 월요일까지 통합 계획
          
       7주차 4/15 ~ 4/19

         * 진행중
          

        * 계획 
           - 알림 추가 기능 -> 안 읽은 알림이 있으면 알려주도록 ui 및 추가 연동 계획.
           - 알림 UI 추가 , 더보기 페이지 구현 계획중.
           - 신용 크레딧 시스템 , 파일 평가 시스템 구축 계획
               == 자신의 협업 진행 상태 업데이트에 대한 사항  ( 크레딧 + 10% 비율 보상이며, 선택제)
               == 자신이 업로드한 파일의 평가 3점기준 (크레딧 + 와 - 35% 비율 보상)
               == 조별과제 협업 히스토리에 대한 크레딧 (크레딧 15% 비율 보상이며, 많을 수록 좋지만 15%비율 이내 적용)
               == 데드라인을 얼마나 지켜내고 있는지 (크레딧 + 와 - 30% 비율 보상) 
               == 어떤 종류의 역할을 하였는지 역할에 따라 크레딧 가중치 다름 ( 크레딧 10% 비율 보상 적용) 
               
               < 점수별 적용 등급 >
               -> 750점 + 이상의 크레딧을 가지고 있으면 excellent credit
               -> 700 - 749점의 크레딧을 가지고 있으면 good credit
               -> 650 - 699점의 크레딧을 가지고 있으면 fair credit
               -> 600 - 649점의 크레딧을 가지고 있으면 poor credit
               -> 600 이하의 크레딧을 가지고 있으면 bad credit 
               
               ===> 이후 , 조원들을 매칭하는 부분에서 점수별로 반영이 가능할 것으로 예상.
               
        * 완료된 사항
           - 파일 리스트 그룹화, 사용자가 속한 과목,팀 정보 볼 수 있도록 완료
           - 알림 기능 그룹화 완료
           - 개발 프로젝트 통합 과정 완료
           - 파일 공유 별점 UI 추가 완료 (db 연동필요)
           - 알림 더보기 기능 UI 추가 완료
           - 전반적인 UI 디자인 수정 완료
           - task 기능 추가 완료
           - 신용 크레딧 시스템 , 파일 평가 시스템 적용을 위한 모델 설계 및 코드 작성 완료 (커밋 확인) 
           - 파일 별점 문서평가 UI 추가 
           
        * 피드백
           - 공유 문서 작성 기능 ui 버그 문제 - 해결 (커밋 확인) 
           - 파일 공유 box 에서 데이터가 없을경우 query matching error 일어남 - 해결  (커밋 확인) 

       8주차 4/22 ~ 4/26
           * 진행중
            - 팀원들의 역할과 과제 진행상황을 자신의 작업상황에 따라 팀원들과 공유할 수 있도록 task 기능과 크레딧 시스템을 추가 및 설계
            - 신용 크레딧 시스템 구현( 자세한 사항은 위의 7주차 내용 참조 ) , 파일 평가 시스템과 크레딧 시스템 연동 적용 진행중 
            
           * 계획 
            - 알림을 더 볼 수 있는 더보기를 구현
            - 평가를 팀원이 하였을 때 알림을 주도록 할 것임 
            - 알림 추가 기능 -> 안 읽은 알림이 있으면 알려주도록 ui 및 추가 연동 계획.
            
           * 완료된 사항
            - 개발 프로젝트 통합 과정 / base.html 상속작업 완료 (extends) 
            - 별점 평가 기능을 db와 연동하여 구현 완료 
            - 파일 공유 평가시스템을 구축 완료 
              (파일에 대한 별점 평가, 코멘트 달 수 있도록 )
            - 파일 검색 기능 구현 완료   
     
            - 자신의 협업 진행상황을 업데이트하는 기능추가 완료 ( db와 연동 완료) 
               * 향후 크레딧 시스템을 적용하기 위함.
               
            - 블록체인 기술 적용을 위한 모델 설계 코드 추가 
               * 향후 크레딧 시스템을 적용하기 위함.
            
           * 기능에 대한 의견
            - 다른 사람이 작성한 문서평가를 볼 수 없다.
            - 팀원들의 문서평가 기록은 교수 등 특정 직위에 있는 admin 만 열람이 가능하다. 
            
   	5. 채팅
       - ~~channels 라이브러리를 이용한 websocket 채팅~~ (04/03)
       - ~~부트스트랩 탬플릿 입히기~~ (04/03)
       - ~~보이스채팅 지원가능한지 찾기~~ > 가능은 하지만 어려움. 시간이 모자라서 굳이 필요할까 싶음. (04/03)
       - 기존 게시판 회원테이블과 연동
       -

-----

### 설치 라이브러리

     	1. django (서버)
   	2. matrix-admin-master (부트스트랩 템플릿 - 메인 UI)
   	3.
