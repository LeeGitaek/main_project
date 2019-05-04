from django import forms
from .models import Team,SubjectAssign

# 클래스정의, Team 모델에 대해서 'team_name', 'project_name', 'text' 필드에 대해서 값을 입력 받겠다는 클래스/폼(form) 정의.
class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ('team_name', 'project_name', 'text')

class SubjectAssignForm(forms.ModelForm):
    class Meta:
        model = SubjectAssign
        fields = ('user_num', 'subject_num')





