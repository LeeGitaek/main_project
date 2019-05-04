from django.urls import path, re_path
from django.conf.urls import include, url
from django.contrib.auth import views as login_views
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('index/', login_views.LoginView.as_view(template_name='registration/login.html'), name='Login'),#웹페이지 첫 템플릿(로그인 템플릿)
    path('mypage/', views.mypage, name='mypage'), #로그인 후 보여지는 마이페이지 템플릿
    path('notice/', views.notice, name='notice'),  # 공지사항 템플릿
    path('board/', views.team_list, name='team_list'), # 과목별 팀 프로젝트 게시판 목록 템플릿
    path('signup/', views.signup, name='Signup'), #회원가입 템플릿
    path('', include('django.contrib.auth.urls'), ), #logout 템플릿
    url(r'^board/(?P<pk>\d+)/$', views.team_detail, name='team_detail'),#팀 프로젝트 게시판 템플릿
    path('team_new/', views.team_new, name='team_new'), #팀 생성 템플릿
    url(r'^team_join/(?P<user_pk>\d+)/(?P<team_pk>\d+)/$', views.team_join, name='team_join'), #팀 가입 템블릿

    # Box app URL CODE start #
    path('box/<teamnum>/<teamname>/uploadto/',views.DocsOfUser), # 업로드
    path('box/',views.userfile),# 자신이 업로드한 파일 리스트
    url(r'^box/board/(?P<pk>\d+)/$', views.boxteam_detail, name='boxteam_detail'),#팀 프로젝트 게시판 템플릿
    # Box app URL CODE end#
    path('chat/', views.chat, name='chat'),
    re_path(r'^chat/(?P<room_name>[^/]+)/$', views.room, name='room'),

    path('subject_assign/', views.subject_assign, name='subject_assign'),  # 로그인 후 보여지는 마이페이지 템플릿
    url(r'^subject_list/(?P<user_pk>\d+)$', views.subject_list, name='subject_list'),

]

# Box file setting code start
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Box file setting code  end
