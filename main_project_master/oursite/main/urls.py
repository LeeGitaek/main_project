
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth import views as login_views
#box app file settings code start #
from django.conf import settings
from django.conf.urls.static import static
#box app file settings code end #
from . import views

urlpatterns = [
   #기본 사이트맵
  #  path('index/', views.index, name='index'), # main/index : 홈페이지(대쉬보드)
    path('board/', views.team_list, name='team_list'), # main/board : 팀프로젝트 게시판
    path('notice/', views.notice, name='notice'), # main/notice : 공지
    path('mypage/', views.mypage, name='mypage'), # main/ect : 기타

#회원가입 관련
    path('signup/', views.signup, name='Signup'),

    path('index/', login_views.LoginView.as_view(template_name='registration/login.html'), name='Login'), #http://127.0.0.1:8000/main/login -> 이 경로로 가면 쟝고 auth 내장 뷰(로그인 로직)와 연결되어 로그인 로직 실행 -> main.login.html 과연동
    path('', include('django.contrib.auth.urls'), ), #logout 페이지 제공

#팀 관련
    url(r'^board/(?P<pk>\d+)$', views.team_detail, name='team_detail'), #path로 하면 오류남 정규식은 url로 해야하는듯
    path('team_new/', views.team_new, name='team_new'),
    url(r'^team_join/(?P<user_pk>\d+)/(?P<team_pk>\d+)/$', views.team_join, name='team_join'), #path로 하면 오류남 정규식은 url로 해야하는듯
# Box app URL CODE start #

    path('box/<username>/<group>/<team>/uploadto/',views.DocsOfUser), # 업로드
    path('box/<username>/<group>/<team>/registertask/',views.registerTask), # task 추가
    path('box/<username>/delete/',views.delete_file), # 파일 삭제
    path('box/<username>/',views.userfile),# 자신이 업로드한 파일 리스트
    path('box/<username>/<group>/<team>/',views.group_file), # 팀원들과 파일공유 가능한
    path('box/<username>/<group>/<team>/score/<revusername>/<revfilename>/',views.document_review), # 평가 스코어
    path('box/<username>/<group>/<team>/<revusername>/<revfilename>/review/',views.document_review_action_handler), # 평가 저장
    path('box/<username>/search/',views.search_documents_action_handler),
    url(r'^box/(?P<username>\w+)/(?P<group>\w+)/(?P<team>\w+)/edit_yourstatus/(?P<edit_pk>\d+)$',views.edit_your_status_handler,name="edits"),
    path('box/<username>/<group>/<team>/edit_yourstatus/update/<mode>/',views.update_status_handler),
# Box app URL CODE end#

]

# Box file setting code start
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Box file setting code  end

'''
import sys
sys.path.insert(0, 'C:/Users/bbwwp/PycharmProjects/main_project/oursite/sharing_docs') # 직접 경로 지정으로 sharing_docs 앱(폴더)를 임포트했다. 파이썬에서 다른 앱(폴더)의 파일을 import 하고 싶으면 이렇게 직접 경로 지정을 해야한다.
from views import board # sharing_docs의 view로부터 board 뷰를 임포트
'''
