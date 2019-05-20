from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.safestring import mark_safe
from django.core.files.storage import FileSystemStorage # file setting code
from .models import Team,Subject_Assign,FileListBox
from .forms import TeamForm,SubjectAssignForm
import datetime as datetime
import json
from django.http import HttpResponse
from .evaluate import Evaluate

def lab(request):
    return render(request,'main/lab.html', {})

def index(request):
    return render(request, 'registration/login.html', {})

def board(request):
    return render(request, 'main/board.html', {})

def notice(request):
    return render(request, 'main/notice.html', {})

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
    return render(request, 'main/find_team.html', {'team_list' : qs, 'subject_num' : tmp})

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
    if request.method == 'POST':
        form = SubjectAssignForm(request.POST, request.FILES)
        if form.is_valid():
          form.save()
          return  redirect('subject_assign')
    else:
        form = SubjectAssignForm()
    return render(request, 'main/subject_edit.html')

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
    return render(request, 'main/team_edit.html', {'subject_num' : subject_pk })

def team_list(request,subject_num):
    qs = Team.objects.all()
    tmp = int(subject_num) #폼으로 넘겨받으면 문자로 받아지기 때문에 int로 형변환해준다. (안해주면 team_list.html에서 if문 동작 안함)
    return render(request, 'main/team_list.html', { 'team_list' : qs, 'subject_num' : tmp })

def team_detail(request, subject_pk, team_pk, hash):
    team = get_object_or_404(Team, pk=team_pk)
    return render(request, 'main/team_detail.html', {'team' : team})
'''
def team_join(request, subject_pk, user_pk, team_pk):
    user = Subject_Assign.objects.get(user_num=user_pk, subject_num = subject_pk)
    user.team_num_id = get_object_or_404(Team, pk=team_pk)
    user.save()
    return render(request, 'main/team_detail.html', {'user': user})
    '''
def team_join(request, subject_pk, user_pk, team_pk, hash):
    user = Subject_Assign.objects.get(user_num=user_pk, subject_num = subject_pk)
    user.team_num_id = get_object_or_404(Team, pk=team_pk)
    user.save()
    # hash = Team.objects.get(pk=team_pk).hash
    return render(request, 'main/team_detail.html', {'user': user})

def userfile(request):
    qs = Team.objects.all()
    return render(request, 'box/box.html',{
            'team_list' : qs,
    })

def boxteam_detail(request, pk):
    team = get_object_or_404(Team, pk=pk)
    all_items = FileListBox.objects.filter(t_num=pk).order_by('-uploaded_date').iterator()
    return render(request, 'box/box_detail.html', {'team' : team,'all_file_items': all_items,})

#box upload function
def DocsOfUser(request,teamnum,teamname):
    if request.method == 'POST' and request.FILES['myfile']:

        now = datetime.datetime.now()
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
        filename = fs.save(myfile.name, myfile)
        filesize =  myfile.size #file size
        uploaded_file_url = fs.url(filename) # file link
        team_title = teamname
        t_num = teamnum
        querys1 = FileListBox(file_name=filename,team_title=team_title,file_size=filesize,t_num=t_num,document=uploaded_file_url,uploaded_date=formatted_date)
        querys1.save()

        return redirect('/main/box/board/'+teamnum)

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

