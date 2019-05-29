from main.models import User,FileListBox,Message,Meeting_Evaluate,Meeting,Subject_Assign,Subject,Team,Post,PostType
from django.http import Http404
from django.contrib.auth.models import User as AuthUser
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect, get_object_or_404
import datetime
import difflib
import os

def addShare(username,teamnum,teamname,files):
    now=datetime.datetime.now()
    formatted_date=now.strftime('%Y-%m-%d %H:%M:%S')
    fs = FileSystemStorage()
    user = User.objects.filter(username__iexact=username).first()

    if user is None:
        raise Http404('User does not exist')

    for f in files:
        tmp = open(os.path.join(os.getcwd(), 'documents', f.name), 'wb+')
        for chunk in f.chunks():
            tmp.write(chunk)
        FileListBox.objects.create(file_name=f.name, team_title=teamname,file_size=f.size, document=fs.url(f.name) ,t_num = teamnum ,uploaded_date=formatted_date)

def AddPost(username,subject_pk,p_pk,p_te,p_ti,p_file):
    now=datetime.datetime.now()
    formatted_date=now.strftime('%Y-%m-%d %H:%M:%S')
    fs = FileSystemStorage()
    user = User.objects.get(username=username)
    subject = get_object_or_404(Subject, pk=subject_pk)
    post_type = get_object_or_404(PostType, pk=p_pk)


    if user is None:
        raise Http404('User does not exist')

    for f in p_file:
        tmp = open(os.path.join(os.getcwd(), 'documents', f.name), 'wb+')
        for chunk in f.chunks():
            tmp.write(chunk)
        Post.objects.create(subject=subject,auth=user,post_type=post_type,title=p_ti,text=p_te,created_date=formatted_date,visit=0,documents=fs.url(f.name),file_name=f.name)
