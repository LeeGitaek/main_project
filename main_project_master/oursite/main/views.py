from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Team
from .forms import TeamForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
import json

#box model import code start #
from django.db.models import Q
from django import template
from django.core.files.storage import FileSystemStorage # file setting code
from .models import FileListBox # model
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

#
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
        filesize = round( myfile.size/1000000 , 1) #file size
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