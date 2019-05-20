from django.urls import path, re_path
from django.conf.urls import include, url
from django.contrib.auth import views as login_views
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('index/', login_views.LoginView.as_view(template_name='registration/login.html'), name='Login'),#첫 페이지(로그인)
    path('', include('django.contrib.auth.urls'),), #로그아웃
    path('signup/', views.signup, name='Signup'),  # 회원가입
    path('mypage/', views.mypage, name='mypage'), #마이페이지
    path('notice/', views.notice, name='notice'),  #공지사항
    path('subject_assignment/', views.subject_assignment, name='subject_assignment'), #과목별 과제 게시판
    path('subject_board/', views.subject_board, name='subject_board'),  #과목별 토론 게시판
    path('subject_notice/', views.subject_notice, name='subject_notice'),  #과목별 공지 게시판

    url(r'^find_team/(?P<subject_pk>\d+)/$', views.find_team, name='find_team'),  # 팀 찾기 게시판

    path('find_team/<subject_pk>/', views.find_team, name='find_team'),  # 팀 찾기 게시판

    url(r'^board/(?P<subject_num>\d+)/$', views.team_list, name='board'),#과목 게시판(board/과목번호)

    url(r'^board/(?P<subject_pk>\d+)/(?P<team_pk>\d+)/(?P<hash>[-\w]+)$', views.team_detail, name='team_detail'),# 팀 게시판(board/과목번호/팀번호)


    url(r'team_new/(?P<subject_pk>\d+)/$', views.team_new, name='team_new'),  #팀 생성(team_new/과목번호)

    url(r'^team_join/(?P<subject_pk>\d+)/(?P<user_pk>\d+)/(?P<team_pk>\d+)/(?P<hash>[-\w]+)$', views.team_join, name='team_join'), #팀 가입(team_join/과목번호/유저번호/팀번호)

    path('subject_assign/', views.subject_assign, name='subject_assign'),  #과목 할당
    url(r'^subject_list/(?P<user_pk>\d+)$', views.subject_list, name='subject_list'), #과목 리스트(subject_list/유저번호)

    path('box/<teamnum>/<teamname>/uploadto/',views.DocsOfUser), # 업로드
    path('box/',views.userfile),# 자신이 업로드한 파일 리스트
    url(r'^box/board/(?P<pk>\d+)/$', views.boxteam_detail, name='boxteam_detail'),#팀 프로젝트 게시판 템플릿

    #채팅 및 평가
    path('chat/', views.chat, name='chat'),
    re_path(r'^chat/(?P<room_name>[^/]+)/$', views.room, name='room'),
    re_path(r'^chat/(?P<room_name>[^/]+)', views.room, name='room'),
    path('evaluate_member/', views.evaluate_member, name='evaluate_member'),
    path('evaluate/', views.evaluate, name='evaluate'),

    path('lab', views.lab, name='lab'),
]

# Box file setting code start
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# Box file setting code  end
