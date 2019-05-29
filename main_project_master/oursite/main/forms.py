from django import forms
from .models import Team,Subject_Assign, Meeting, Meeting_Evaluate, Subject, Post, Comment
from django.forms import DateTimeInput

# 클래스정의, Team 모델에 대해서 'team_name', 'project_name', 'text' 필드에 대해서 값을 입력 받겠다는 클래스/폼(form) 정의.
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('subject_num', 'team_name', 'project_name', 'text', 'hash')

class SubjectAssignForm(forms.ModelForm):
    class Meta:
        model = Subject_Assign
        fields = ('user_num', 'subject_num')

class MeetingForm(forms.ModelForm):
    date_start = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'name': 'date_start'},
            format='%Y-%m-%dT%H:%M')
    )
    date_end = forms.DateTimeField(
        input_formats=['%Y-%m-%dT%H:%M'],
        widget=forms.DateTimeInput(
            attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'name': 'date_end'},
            format='%Y-%m-%dT%H:%M')
    )
    class Meta:
        model = Meeting
        fields = ('title', 'date_start', 'date_end', 'team_num', 'meeting_num', 'hash')

class MeetingEvaluateForm(forms.ModelForm):
    class Meta:
        model = Meeting_Evaluate
        fields = ('evaluate', 'team_num', 'meeting_num', 'user_from', 'user_num')

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ('num', 'subject_name', 'prof')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)