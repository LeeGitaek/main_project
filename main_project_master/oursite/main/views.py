from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team
from .forms import TeamForm
from django.contrib.auth.models import User

#box model import code start #
from django.db.models import Q
from django import template
from django.core.files.storage import FileSystemStorage # file setting code
from .models import FileListBox # model
from .models import NotificationBox # model
from .models import Subject # 공통코드 부분
from .models import TaskBox # model
from .models import ReviewBox # model
import datetime as datetime
import os # os
#box model import code end #

def index(request):
    return render(request, 'main/index.html', {})

def board(request):
    return render(request, 'main/board.html', {})

def notice(request):
    return render(request, 'main/notice.html', {})

def mypage(request):
    return render(request, 'main/mypage.html', {})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('mypage')
    else:
        form = UserCreationForm()
    return render(request, 'main/signup.html', {'form': form})

def team_new(request):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
          form.save()
          return  redirect('team_list')
    else:
        form = TeamForm()
    return render(request, 'main/team_edit.html')

def team_list(request):
    qs = Team.objects.all()
    return render(request, 'main/team_list.html', { 'team_list' : qs })

def team_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    return render(request, 'main/team_detail.html', {'team' : team})

def team_join(request, user_pk, team_pk):
    user = User.objects.get(pk=user_pk)
    user.userteam.team_num = get_object_or_404(Team, pk=team_pk)
    user.save()
    team = get_object_or_404(Team, pk=team_pk)
    return render(request, 'main/team_detail.html', {'team': team})

def userfile(request,username):
    all_items = FileListBox.objects.filter(user_name=username).order_by('-uploaded_date').iterator() # 파일리스트 쿼리셋  메모리 쿼리 절약 캐싱
    querysub1 = Subject.objects.get(userid=username)
    querysub2 = querysub1.subject_name
    all_notify = NotificationBox.objects.filter(uploaded_teamtitle=querysub2).order_by('-uploaded_datetime').iterator() # 알림 쿼리셋 메모리 쿼리 절약 캐싱
    all_group = Subject.objects.filter(userid=username).order_by('-created_date').iterator() # 그룹 정보
    all_review = ReviewBox.objects.filter(review_er=username).order_by('-review_date').iterator() # 평가 기록

    if not all_items:
         return render(request, 'box/box.html',{
            #'all_file_items': all_items,
            #'all_notification': all_notify,
            'user':username,
            #'all_groups':all_group,
            #'all_reviews':all_review,
         })
    else :
        return render(request, 'box/box.html',{
            'all_file_items': all_items,
            'all_notification': all_notify,
            'user':username,
            'all_groups':all_group,
            'all_reviews':all_review,
        })

#box grouping. box/username/group/team/
def group_file(request,username,group,team):
    all_items = FileListBox.objects.filter(class_name=group,t_num=team).order_by('-uploaded_date').iterator() # 파일리스트 쿼리셋  메모리 쿼리 절약 캐싱
    all_notify = NotificationBox.objects.filter(uploaded_teamtitle=group).order_by('-uploaded_datetime').iterator() # 알림 쿼리셋 메모리 쿼리 절약 캐싱
    all_group = Subject.objects.filter(userid=username).order_by('-created_date').iterator() # 그룹 정보
    all_task = TaskBox.objects.filter(task_subject=group,task_team=team).order_by('-task_dead').iterator() # task

    if not all_items:
         return render(request, 'box/box.html',{
            #'all_file_items': all_items,
            'all_notification': all_notify,
            'user':username,
            'all_groups':all_group,
            'group':group,
            'team':team,
         })
    else :
        if not all_task:
                return render(request, 'box/box.html',{
                    #'all_file_items': all_items,
                    'all_notification': all_notify,
                    'user':username,
                    'all_groups':all_group,
                    'group':group,
                    'team':team,
                    #'all_tasks':all_task,
                 })
        return render(request, 'box/box.html',{
            'all_file_items': all_items,
            'all_notification': all_notify,
            'user':username,
            'all_groups':all_group,
            'group':group,
            'team':team,
            'all_tasks':all_task,
        })


#box delete file
def delete_file(request,username):    # delete file action.
    if request.method == 'POST' and request.POST['del']:
        file_name_del = request.POST['del']
        del_in = FileListBox.objects.filter(id=file_name_del).delete()

        return redirect('/main/box/'+username)

#box upload function
def DocsOfUser(request,username,group,team):
    if request.method == 'POST' and request.FILES['myfile']:
        user_name = username
        now = datetime.datetime.now()
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        filename = fs.save(myfile.name, myfile)
        filesize = round( myfile.size/1000000 , 1) #file size
        uploaded_file_url = fs.url(filename) # file link
        class_name = group # 과목 이름
        groupinfo = Team.objects.get(subject_num=team) # 그룹 정보
        team_title = groupinfo.team_name #group_info.numberof_group
        user = User.objects.filter(username=user_name) # get a group information
        t_num = team #group_info.groupId # user's group id.
        #user_rate = 1200.00  # user's rating / basic 1200
        #weights_num = 0.84 # call change rate function
        assignment_title = groupinfo.project_name
        #document_similarity = 0.0
        #reward_score = 0.0
        querys1 = FileListBox(file_name=filename,class_name=class_name,team_title=team_title,user_name=user_name,assignment_title=assignment_title,file_size=filesize,t_num=t_num,document=uploaded_file_url,uploaded_date=formatted_date)
        querys1.save()

        querys2 = NotificationBox(uploaded_filename=filename,uploaded_account=user_name,uploaded_teamtitle=group,edited_orwhat='0',read_ox='0',uploaded_groupid=t_num,uploaded_datetime=formatted_date)
        querys2.save()


        #user.userteam.xn_rating = weights_num
        #user.save()

        return redirect('/main/box/'+user_name+'/'+group+'/'+team)

# register task
def registerTask(request,username,group,team):
    if request.method == 'POST' and request.POST['taskuser']:
        user_task = request.POST['taskuser']    #사용자
        name_task = request.POST['taskname']     # taskname task
        ch_task = request.POST['taskch']     # taskch 진행상황
        status_task = request.POST['taskstatus'] # taskstatus 퍼센트
        date_task = request.POST['taskdate'] # taskdate 데드라인

        registertask_query = TaskBox(task_user=user_task , task_role=name_task, task_status = ch_task, task_percent = status_task,task_dead=date_task,task_subject=group,task_team=team)
        registertask_query.save()
        return redirect('/main/box/'+username+'/'+group+'/'+team)

# 파일 평가 기능 구현 함수 작성중.
# box/<username>/<group>/<team>/score/<revusername>/<revfilename>/
def document_review(request,username,group,team,revusername,revfilename):
    return render(request, 'box/box_review.html',{
        'revusername':revusername,
        'revfilename':revfilename,
        'user':username,
        'group':group,
        'team':team,
    })

# /main/box/{{user}}/group/team/{{ file_item.user_name }}/{{ file_item.file_name }}/review/
def document_review_action_handler(request,username,group,team,revusername,revfilename):
    if request.method == 'POST' and request.POST['revusername']:
        review_username = request.POST['revusername'] # 파일 올린 사용자
        review_filename = request.POST['revfilename'] # 파일 이름
        review_group = request.POST['subject'] # 과목
        review_team = request.POST['teamid'] # 팀 그룹
        review_er = request.POST['userid'] # 평가하는 사용자
        review_score = request.POST['score'] # 평가 점수
        review_comments = request.POST['comments'] # 평가 피드백
        registerReview_query = ReviewBox(review_file=review_filename,review_uploader=review_username,review_subject=review_group,review_team=review_team,review_er=review_er,review_score=review_score,review_comments=review_comments)
        registerReview_query.save()
        return redirect('/main/box/'+username+'/'+group+'/'+team)

    #/main/box/{{user}}/{{group}}/{{team}}/score/{{ file_item.user_name }}/{{ file_item.file_name }}/
    #if request.method == 'POST' and request.POST['rev_score']:
# /main/box/{{user}}/search
def search_documents_action_handler(request,username):
    if request.method == 'POST' and request.POST['search']:
        querysub1 = Subject.objects.get(userid=username)
        querysub2 = querysub1.subject_name
        all_notify = NotificationBox.objects.filter(uploaded_teamtitle=querysub2).order_by('-uploaded_datetime').iterator()
        searchkey = request.POST['search']
        result = '검색 결과 없음. 파일이 없네요 ㅠ '
        querysearching1 = Subject.objects.get(userid=username)
        querysearching2 = querysearching1.team_num_id
        all_search = FileListBox.objects.filter( Q(file_name__icontains=searchkey),t_num=querysearching2).order_by('-uploaded_date').distinct().iterator() # 파일리스트 쿼리셋  메모리 쿼리 절약 캐싱

        if not all_search:
             return render(request, 'box/box_search.html',{
            #    'all_search_items': all_search,
                'all_notification': all_notify,
                'user':username,
                'result':result,
                'keyw':searchkey,
             })
        else :
            return render(request, 'box/box_search.html',{
                'all_search_items': all_search,
                'all_notification': all_notify,
                'user':username,
                #'result':result,
                'keyw':searchkey,
            })

