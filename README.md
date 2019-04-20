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
          - 파일 리스트 그룹화,알림 기능 그룹별 연동 진행할 계획, 사용자가 속한 그룹 정보 볼 수 있도록 수정 등 진행중..
          - 월요일까지 통합 계획

       * 계획
          - 알림 추가 기능 -> 안 읽은 알림이 있으면 알려주도록 ui 및 추가 연동 계획.


       * 완료된 사항
          - 알고리즘 코드 모두 삭제.
          - 파일 delete 버튼 추가 및 연동 그리고 버그수정 완료.
          - 파일 업로드는 과목을 선택한 후에 가능하도록 하였음.

       7주차 4/15 ~ 4/19

         * 진행중
           - 파일 공유 별점 db 연동 진행중.

        * 계획
           - 디자인 수정계획
           - 알림 추가 기능 -> 안 읽은 알림이 있으면 알려주도록 ui 및 추가 연동 계획.
           - 알림 UI 추가 , 더보기 페이지 구현 계획중.

        * 완료된 사항
           - 파일 리스트 그룹화, 사용자가 속한 과목,팀 정보 볼 수 있도록 완료
           - 알림 기능 그룹화 완료
           - 개발 프로젝트 통합 과정 완료
           - 파일 공유 별점 UI 추가 완료 (db 연동필요)
           - 알림 더보기 기능 UI 추가 완료
        * 피드백
           - 공유 문서 작성 기능 ui 버그 문제 - 해결 (커밋 확인) 
           - 파일 공유 box 에서 데이터가 없을경우 query matching error 일어남 - 해결  (커밋 확인) 


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
