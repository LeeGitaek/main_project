from django.contrib import messages
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.core.files.storage import FileSystemStorage # file setting code
from main import datafunction
from .models import Team,Subject_Assign,FileListBox, Subject, Meeting, Meeting_Evaluate, Post, Subject, Comment, PostType
from .forms import TeamForm,SubjectAssignForm, MeetingForm, MeetingEvaluateForm, PostForm, SubjectForm, CommentForm

import datetime as datetime
import json
from django.http import HttpResponse
from .evaluate import Evaluate
from django.core.exceptions import ObjectDoesNotExist

def lab(request):
    return render(request,'main/lab.html', {})

def board(request):
    return render(request, 'main/board.html', {})

def notice(request):
    post = Post.objects.all()
    return render(request, 'main/notice.html',
                  {
                      'post': post,
                  })

@login_required(login_url='/main/index/')
def mypage(request):
    return render(request, 'main/mypage.html', {})

def subject_assignment(request):
    return render(request, 'main/subject_assignment.html', {})

def subject_board(request):
    return render(request, 'main/subject_board.html', {})

def subject_notice(request):
    return render(request, 'main/subject_notice.html', {})

def find_team(request,subject_pk):
    qs = Team.objects.all()
    tmp=int(subject_pk)
    subject_name = Subject.objects.get(pk=subject_pk).subject_name
    return render(request, 'main/find_team.html', {'team_list' : qs, 'subject_pk' : tmp, 'subject_name' : subject_name})

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

def subject_assign(request):
    subjects = Subject.objects.all()
    if request.method == 'POST':
        form = SubjectAssignForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return  redirect('subject_assign')
    else:
        form = SubjectAssignForm()
    return render(request, 'main/subject_edit.html',
    {
        'subjects': subjects,
    })

def subject_list(request, user_pk):
    qs = Subject_Assign.objects.filter(user_num = user_pk)
    return render(request, 'main/subject_list.html', { 'subject_list' : qs })

def team_new(request, subject_pk):
    if request.method == 'POST':
        form = TeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('find_team', subject_pk)
    else:
        form = TeamForm()
    return render(request, 'main/team_edit.html', {'subject_pk' : subject_pk, 'team_pk': 1 })

def team_list(request,subject_pk):
    qs = Team.objects.all()
    tmp = int(subject_pk) #폼으로 넘겨받으면 문자로 받아지기 때문에 int로 형변환해준다. (안해주면 team_list.html에서 if문 동작 안함)
    return render(request, 'main/team_list.html', { 'team_list' : qs, 'subject_pk' : tmp })

def team_detail(request, subject_pk, team_pk, meeting_num, hash):
    team = get_object_or_404(Team, pk=team_pk)
    return render(request, 'main/team_detail.html', {'team' : team})

def team_join(request, subject_pk, user_pk, team_pk):
    user = Subject_Assign.objects.get(user_num=user_pk, subject_num = subject_pk)
    user.team_num_id = get_object_or_404(Team, pk=team_pk)
    user.save()
    # hash = Team.objects.get(pk=team_pk).hash
    return render(request, 'main/meeting_list.html', {'subject_pk': subject_pk, 'team_pk': team_pk, 'user': user})

#파일 공유 페이지 시작
def userfile(request):
    qs = Team.objects.all()
    return render(request, 'box/box.html',{
            'team_list' : qs,
    })

def boxteam_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    all_items = FileListBox.objects.filter(t_num=pk).order_by('-uploaded_date').iterator()
    return render(request, 'box/box_detail.html', {'team' : team,'all_file_items': all_items,})


def addreq_project(request, username , teamnum, teamname):
    files = request.FILES.getlist('files[]')
    datafunction.addShare(username,teamnum,teamname, files)
    return redirect('/main/box/board/'+teamnum)

def post_cloud(request,username,subject,subject_pk,p_pk):
    p_te = request.POST['p_title']
    p_ti = request.POST['p_text']
    p_file = request.FILES.getlist('cl[]')
    datafunction.AddPost(username,subject_pk,p_pk,p_te,p_ti,p_file)
    return file_board(request,pk=subject_pk)

#파일 공유 페이지 끝

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'username' : mark_safe(json.dumps(request.user.username)),
    })

def chat(request):
    return render(request, 'chat/index.html', {})

def evaluate(request):
    user_pk = User.objects.get(username=request.user.username).id
    Evaluate.evalMessage(Evaluate, user_pk, 2)
    return render(request, 'main/team_evaluate.html', {'username' : mark_safe(json.dumps(request.user.username))})

def evaluate_member(request):
    data = {
        'mem1': '박병욱',
        'mem2': '이기택',
        'mem3': '엄태선'
    }
    return HttpResponse(json.dumps(data), content_type="application/json")

def meeting_list(request,subject_pk, team_pk):
    meetings = Meeting.objects.filter(team_num=team_pk)
    tmp = int(subject_pk) #폼으로 넘겨받으면 문자로 받아지기 때문에 int로 형변환해준다. (안해주면 team_list.html에서 if문 동작 안함)
    subject_name = Subject.objects.get(pk=subject_pk).subject_name
    team_name = Team.objects.get(pk=team_pk).team_name
    return render(request, 'main/meeting_list.html', { 'meeting_list' : meetings, 'subject_pk' : tmp, 'subject_name': subject_name, 'team_pk': team_pk, 'team_name': team_name})

def meeting_join(request, subject_pk, user_pk, team_pk, meeting_num, hash):
    return render(request, 'main/team_detail.html', {'user': '12344'})

def meeting_new(request, subject_pk, team_pk):
    try:
        a = Meeting.objects.filter(team_num=1).count()
        meeting_num = a + 1
    except ObjectDoesNotExist:
        meeting_num = 1

    if request.method == 'POST':
        form = MeetingForm(request.POST, request.FILES)
        if form.is_valid():
            print('제출됨!!')
            form.save()
            return redirect('meeting_list', subject_pk=subject_pk, team_pk=team_pk)
        print('제출안됨;;')
    else:
        form = MeetingForm()
    return render(request, 'main/meeting_edit.html', {'subject_pk' : subject_pk, 'team_pk' : team_pk, 'meeting_num': meeting_num })


# 과목 관리
@login_required
def manage_subjetct(request):
    subjects = Subject.objects.all()
    posts =Post.objects.all()
    qs = Subject_Assign.objects.all()
    return render(request, 'post/manage_subject.html',
                  {
                      'subjects':subjects,
                      'posts':posts,
                      'qs': qs
                  })

# 과목 생성
@login_required
def manage_subject_new(request):
    if request.method == "POST":
        form = SubjectForm(request.POST)

        if form.is_valid():
            subject = form.save(commit = False)
            subject.auth = request.user
            subject.save()

            return redirect('manage_subject')

    else:  # elif request.method == "GET": ## 겟인 경우
        form = SubjectForm()  # 모든 과목리스트를 리턴한다.

    return render(request, 'post/manage_subject_new.html',
                      {
                          'form':form
                      })

# 과목 삭제
@login_required
def manage_subject_remove(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    subject.delete()
    return redirect('manage_subject')

# 게시판
def subject(request, pk=None):
    subject=Subject.objects.get(pk=pk) # 과목 번호만 받아준다
    post_types=PostType.objects.all()
    post=Post.objects.all()
    qs = Team.objects.all()
    tmp = int(pk)  # 폼으로 넘겨받으면 문자로 받아지기 때문에 int로 형변환해준다. (안해주면 team_list.html에서 if문 동작 안함)
    results=[]  # 과연 필요한가?
    for post_type in post_types:
        posts = Post.objects.filter(post_type=post_type, subject=subject)[:5]
        results.append(
            {
                "post_type":post_type,
                "posts":posts
            }
        )

    return render(request, 'post/subject.html',
                  {
                      'subject':subject,
                      'results':results,
                      'post':post,
                      'post_types':post_types,
                      'team_list': qs,
                      'subject_pk': tmp
                  })

#타입별 게시판
@login_required
def board(request, pk=None, pt=None):
    subject=get_object_or_404(Subject, pk=pk)
    post_type=get_object_or_404(PostType, pk=pt)
    post=Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date') # 만들어진시각__보다같거나작은=현재시간
    return render(request, 'post/board.html',
                  {
                      'post':post,
                      'subject':subject,
                      'post_type':post_type,
                  })

# 공지 게시판 # 관리자 모드일 때만 글 생성이 가능하도록
@login_required
def notice_board(request, pk=None):
    subject = get_object_or_404(Subject, pk=pk)
    post = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date') # 만들어진시각__보다같거나작은=현재시간
    post_type=PostType.objects.get(pk = 1)

    paginator = Paginator(post, 3) #5개까지만 보여줄 수 있도록
    page = request.GET.get('page') # page에 page값을 GET하는 request값을 저장해준다
    # request 값은 POST와 GET을 받아올 수 있는데, POST는 글을 수정/삭제 할 때 사용하고 GET은 객체를 받아올 때 주로 사용한다.
    posts = paginator.get_page(page)

#    try:
#        posts = paginator.page(page)
#    except PageNotAnInteger:
#        posts = paginator.page(1)
#    except EmptyPage:
#        posts = paginator.page(paginator.num_pages)

    return render(request, 'post/notice.html',
                  {
                      'post': post,
                      'subject': subject,
                      'post_type': post_type,
                      #'posts': posts
                  }
    ) #post함수는 post/post.html로 가준다

@login_required
def file_board(request, pk=None):
    subject = get_object_or_404(Subject, pk=pk)
    post = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date') # 만들어진시각__보다같거나작은=현재시간
    post_type=PostType.objects.get(pk = 3)

    paginator = Paginator(post, 3) #5개까지만 보여줄 수 있도록
    page = request.GET.get('page') # page에 page값을 GET하는 request값을 저장해준다
    # request 값은 POST와 GET을 받아올 수 있는데, POST는 글을 수정/삭제 할 때 사용하고 GET은 객체를 받아올 때 주로 사용한다.
    posts = paginator.get_page(page)

#    try:
#        posts = paginator.page(page)
#    except PageNotAnInteger:
#        posts = paginator.page(1)
#    except EmptyPage:
#        posts = paginator.page(paginator.num_pages)

    return render(request, 'post/file.html',
                  {
                      #'post': post,
                      'subject': subject,
                      'post_type': post_type,
                      'posts': posts,
                      'sub_pk':pk,
                  }
    ) #post함수는 post/post.html로 가준다

# 토론 게시판
@login_required
def debate_board(request, pk=None,):
    subject = get_object_or_404(Subject, pk=pk)
    post = Post.objects.filter(created_date__lte=timezone.now()).order_by('created_date') # 만들어진시각__보다같거나작은=현재시간
    post_type=PostType.objects.get(pk = 2)
    return render(request, 'post/debate.html',
                  {
                      'post': post,
                      'subject': subject,
                      'post_type': post_type
                  }
    ) #post함수는 post/post.html로 가준다


#게시물
def post(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    subject = Subject.objects.all()

    return render(request, 'post/post.html',
                  {
                      'post':post,
                      'subject':subject,
                  })

#게시물 생성
@login_required
def post_new(request, subject_pk, pt):
    subject = get_object_or_404(Subject, pk=subject_pk)
    post_type = get_object_or_404(PostType, pk=pt)
    if request.method == "POST":
        form=PostForm(request.POST)
        if form.is_valid(): # 만약 form이 사용 가능할 때
            post = form.save(commit=False)
            post.subject=subject
            post.post_type = post_type
            post.auth=request.user
            post.save()
            return redirect('post', pk=post.pk)
    else:
        form=PostForm()

    return render(request, 'post/post_new.html',
                  {
                      'form':form
                  })

#게시물 수정
@login_required
def post_edit(request, pk):
    post=get_object_or_404(Post, pk=pk)
    if post.auth != request.user:
        messages.success(request, '권한이 없습니다 ㅠㅠ')
        return redirect('post', pk=post.pk)

    if request.method == "POST":
        form = PostForm(request.POST, instance=post) #이미 저장된 인스턴스 정보를 객체에 넣어준다

        if form.is_valid():
            post=form.save(commit=False)
            post.auth=request.user
            post.save()
            return redirect('post', pk=post.pk) #수정이 된 객체는 post.pk번

    else:
        form=PostForm(instance=post)

    return  render(request, 'post/post_new.html',
                   {
                       'form':form
                   })

#게시물 삭제
@login_required
def post_remove(request, pk, subject_pk):
    post=get_object_or_404(Post, pk=pk)
    subject = get_object_or_404(Subject, pk=subject_pk)

    if post.auth != request.user:
        messages.success(request, '권한이 없습니다 ㅠㅠ')
        return redirect('post', pk=pk)

    post.delete()
    return redirect('subject', subject_pk)

#댓글 달기
@login_required
def comment_new(request, post_pk):
    post=get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.auth = request.user
            comment.save()
            return redirect('post', pk=post.pk)

    else:
        form = CommentForm()

    return render(request, 'post/comment_edit.html',
                  {
                      'form':form
                  })

# 댓글 수정
@login_required
def comment_edit(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=pk)

    if comment.auth != request.user:
        messages.success(request, '권한이 없습니다 ㅠㅠ')
        return redirect('post', pk=post.pk)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = comment.save()
            return redirect('post', pk=post.pk)

    else:
        form = CommentForm(instance=comment)

    return render(request, 'post/comment_edit.html',
                  {
                      'form': form
                  })

# 댓글 삭제
@login_required
def comment_remove(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=pk)

    if comment.auth != request.user:
        messages.success(request, '권한이 없습니다 ㅠㅠ')
        return redirect('post', pk=post.pk)

    comment.delete()

    return redirect('post', pk=post.pk)

@login_required
def subject_assign_remove(request):
    return render(request, 'main/subject_assign_remove.html')

@login_required
def subject_assign_delete(request, pk):
    subject = Subject_Assign.objects.get(subject_num=pk)

    subject.delete()
    return render(request, 'main/subject_assign_remove.html')
