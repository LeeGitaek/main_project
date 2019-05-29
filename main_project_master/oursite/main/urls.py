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

# 과목 관리
    path('manage_subject/', views.manage_subjetct, name='manage_subject'),  # 과목 관리 게시판
    path('manage_subject/new/', views.manage_subject_new, name='manage_subject_new'),  # 과목 생성 게시판
    path('manage_subject_remove/<int:pk>/', views.manage_subject_remove, name='manage_subject_remove'),  # 게시물 삭제
    path('subject/<int:pk>/', views.subject, name='subject'),  # 과목 게시판
    path('subject_assign/remove', views.subject_assign_remove, name='subject_assign_remove'), # 할당 해제
    path('subject_assign/remove/<pk>', views.subject_assign_delete, name='subject_assign_delete'), # 할당 해제

    path('subject/<int:pk>/<int:pt>/', views.board, name='board'),  # 공지/과제/토론 게시판

    path('subject/<int:pk>/notice/', views.notice_board, name='notice_board'),  # 공지게시판
    path('subject/<int:pk>/debate/', views.debate_board, name='debate_board'),  # 토론게시판
    path('subject/<int:pk>/file/', views.file_board, name='file_board'),  # 파일게시판

    # 게시판 관리
    path('post/<int:pk>/', views.post, name='post'),  # 게시물
    path('subject/<int:subject_pk>/<int:pt>/new/', views.post_new, name='post_new'),  # 게시물 생성
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),  # 게시물 수정
    path('post/<int:pk>/<int:subject_pk>/remove/', views.post_remove, name='post_remove'),  # 게시물 삭제

    # 댓글 관리
    re_path(r'^(?P<post_pk>\d+)/comment/new/$', views.comment_new, name='comment_new'), # 댓글달기 / html은 있지만 post_detail 중간에 삽입되어있음
    re_path(r'^(?P<post_pk>\d+)/comment/(?P<pk>\d+)/edit/$', views.comment_edit, name='comment_edit'),  # 댓글 수정
    re_path(r'^(?P<post_pk>\d+)/comment/(?P<pk>\d+)/remove/$', views.comment_remove, name='comment_remove'),  # 댓글 삭제

    path('find_team/subject_pk>/', views.find_team, name='find_team'),  # 팀 찾기 게시판
    path('find_team/<subject_pk>/', views.find_team, name='find_team'),  # 팀 찾기 게시판

    path('board/<subject_pk>/', views.team_list, name='board'),#과목 게시판(board/과목번호)

    url(r'^board/(?P<subject_pk>\d+)/(?P<team_pk>\d+)/(?P<meeting_num>\d+)/(?P<hash>[-\w]+)$', views.team_detail, name='team_detail'),# 팀 게시판(board/과목번호/팀번호)
    path('board/<subject_pk>/<team_pk>/', views.meeting_list, name='meeting_list'),# 팀 게시판(board/과목번호/팀번호)
    url(r'^meeting_join/(?P<subject_pk>\d+)/(?P<user_pk>\d+)/(?P<team_pk>\d+)/(?P<meeting_num>\d+)/(?P<hash>[-\w]+)$', views.meeting_join, name='meeting_join'),  # 팀 가입(team_join/과목번호/유저번호/팀번호)
    path('team_join/<subject_pk>/<user_pk>/<team_pk>/', views.team_join, name='team_join'), #팀 가입(team_join/과목번호/유저번호/팀번호)
    path('team_new/<subject_pk>/', views.team_new, name='team_new'),  # 팀 생성(team_new/과목번호)

    path('meeting_new/<subject_pk>/<team_pk>/', views.meeting_new, name='meeting_new'),  #회의 생성(team_new/과목번호)

    path('subject_assign/', views.subject_assign, name='subject_assign'),  #과목 할당
    path('subject_list/<user_pk>/', views.subject_list, name='subject_list'), #과목 리스트(subject_list/유저번호)

     #path('box/<teamnum>/<teamname>/uploadto/',views.DocsOfUser), # 업로드
    re_path(r'^addreq_projects/(?P<username>[\w_]{3,50})/(?P<teamnum>\d+)/(?P<teamname>[\w_]{3,50})/$',views.addreq_project,name="addreq_project"),
    re_path(r'^addreq_post/(?P<username>[\w_]{3,50})/(?P<subject>[\w_]{3,50})/(?P<subject_pk>\d+)/(?P<p_pk>\d+)/$',views.post_cloud,name="addreq_post"),
    path('box/',views.userfile,name='box'),# 자신이 업로드한 파일 리스트
    url(r'^box/board/(?P<pk>\d+)', views.boxteam_detail, name='boxteam_detail'),#팀 프로젝트 게시판 템플릿

    path('chat/', views.chat, name='chat'),  #채팅 및 평가

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
