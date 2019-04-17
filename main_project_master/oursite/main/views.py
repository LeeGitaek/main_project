from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team
#box model import code start #
from django.core.files.storage import FileSystemStorage # file setting code
from .models import FileListBox # model
from .models import NotificationBox # model
import numpy as np # math
import os # os
#box model import code end #
from .forms import TeamForm
from django.contrib.auth.models import User
#홈 페이지
def index(request):
    return render(request, 'main/index.html', {})

def board(request):
    return render(request, 'main/board.html', {})

def notice(request):
    return render(request, 'main/notice.html', {})

def mypage(request):
    return render(request, 'main/mypage.html', {})

#회원가입 뷰
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('mypage') #회원가입 완료하면 홈페이지로 리다이렉팅
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

#팀 생성 뷰
def team_new(request):
    if request.method == 'POST': #포스트 방식으로 넘김 받는다면
        form = TeamForm(request.POST, request.FILES) #forms.py에서 정의한 TeamForm에 POST로 받은 request.POST, request.FILES 데이터 저장
        if form.is_valid():
          form.save()
          return  redirect('team_list')
    else:
        form = TeamForm() #현재 요청이 'POST'가 아니라면 빈 폼을 보여준다.
    return render(request, 'main/team_edit.html')

#팀 목록 출력 뷰
def team_list(request):
    qs = Team.objects.all() #Team 테이블의 모든 객체를 받아옴
    return render(request, 'main/team_list.html', { 'team_list' : qs }) #받아온 모든 Team 객체를 'team_list'란 이름을 부여하여 team_list.html 템플릿으로 넘겨준다.

#팀 상세 내역 뷰(팀 게시판 역할)
def team_detail(request, pk):  #pk를 인자로 받아서
    team = get_object_or_404(Team, pk=pk)  #Team 테이블의 pk를 primary key로 갖는 튜플을 뽑아서(만족하는 튜플이 없으면 404 에러)
    return render(request, 'main/team_detail.html', {'team' : team}) #'team' 이란 이름으로 team_detail.html 에 보낸다.

#팀 가입 뷰
def team_join(request, user_pk, team_pk): #템플릿 ~ urls로부터 user의 pk와 team의 pk를 받아온다.
    user = User.objects.get(pk=user_pk)  #현재 로그인한 user의 객체를 가져온다.
    user.userteam.team_num = get_object_or_404(Team, pk=team_pk) #유저의 team_num 속성에 team의 pk를 사용하여 참조한 팀 객체를 넣어준다. 주키를 넣어주면 동작안함!!(SQL join)
    user.save()
    team = get_object_or_404(Team, pk=team_pk)
    return render(request, 'main/team_detail.html', {'team': team})
   #return render(request, 'main/test.html', { 'id' : pk, 'team_num' : team })

#SQL join 관련하여 알아둘것 : 외래키에 값을 넣어줄때 참조받는 테이블의 주키를 넣어주는게 아니라 그 튜플 객체 자체를 넘겨줘야한다.

## DEVELOPER : 이기택
## BOX APP
## Box 박스 앱 VIEWS CODE START ##
## 2019/04/16 15:46 MOVED ##

#box/username list
def userfile(request,username):
    all_items = FileListBox.objects.filter(user_name=username).order_by('-uploaded_date').iterator() # 파일리스트 쿼리셋  메모리 쿼리 절약 캐싱
    all_notify = NotificationBox.objects.order_by('-uploaded_datetime').iterator() # 알림 쿼리셋 메모리 쿼리 절약 캐싱
    #all_group = Subject.objects.filter(usernum_Ingroup=username).order_by('-join_date').iterator() # 그룹 정보

    if not all_items:
         return render(request, 'box/box.html',{
            #'all_file_items': all_items,
            'all_notification': all_notify,
            'user':username,
            #'all_groups':all_group,
         })
    else :
        return render(request, 'box/box.html',{
            'all_file_items': all_items,
            'all_notification': all_notify,
            'user':username,
        #    'all_groups':all_group,
        })

#box grouping. box/username/group
def group_file(request,username,group):
    all_items = FileListBox.objects.filter(user_name=username).order_by('-uploaded_date').iterator() # 파일리스트 쿼리셋  메모리 쿼리 절약 캐싱
    all_notify = NotificationBox.objects.order_by('-uploaded_datetime').iterator() # 알림 쿼리셋 메모리 쿼리 절약 캐싱

    if not all_items:
         return render(request, 'box/box.html',{
            #'all_file_items': all_items,
            'all_notification': all_notify,
            'user':username,
            'group':group,
         })
    else :
        return render(request, 'box/box.html',{
            'all_file_items': all_items,
            'all_notification': all_notify,
            'user':username,
            'group':group,
        })


#box delete file
def delete_file(request,username):    # delete file action.
    if request.method == 'POST' and request.POST['del']:
        file_name_del = request.POST['del']
        del_in = FileListBox.objects.filter(id=file_name_del).delete()

        return redirect('http://127.0.0.1:3000/box/'+username)

#box upload function
def DocsOfUser(request,username,group):
    if request.method == 'POST' and request.FILES['myfile']:
        user_name = username
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename) # file link
        #group_info = #GroupInformation.objects.get(usernum_Ingroup = user_name)
        class_name = group # 과목 이름
        team_title = "프로젝트"#group_info.numberof_group
        user = User.objects.filter(username=user_name) # get a group information
        t_num = "142"#group_info.groupId # user's group id.
        #user_rate = 1200.00  # user's rating / basic 1200
        #weights_num = 0.84 # call change rate function
        #team_info = Team.objects.get(num=t_num)
        assignment_title = group
        #file_size = os.path.getsize(uploaded_file_url)
        #document_similarity = 0.0
        #reward_score = 0.0
        querys1 = FileListBox(file_name=filename,class_name=class_name,team_title=team_title,user_name=user_name,assignment_title=assignment_title,file_size=0,t_num=t_num,document=uploaded_file_url)
        querys1.save()

        querys2 = NotificationBox(uploaded_filename=filename,uploaded_account=user_name,uploaded_teamtitle=team_title,edited_orwhat='0',read_ox='0',uploaded_groupid=t_num)
        querys2.save()


        #user.userteam.xn_rating = weights_num
        #user.save()

        return redirect('http://127.0.0.1:4000/main/box/'+user_name)

# document_similarity calculation
def document_similarity_cal():
    print('Hello!')


## Box 박스 앱 VIEWS CODE END ##
## DEVELOPER : 이기택
## BOX APP
## 2019/04/16 15:46 MOVED ##
