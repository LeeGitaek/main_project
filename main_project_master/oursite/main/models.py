from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

class Subject(models.Model):
    num = models.IntegerField(primary_key=True)  # 과목 번호(주키)
    subject_name = models.CharField(max_length=100)  # 과목 이름

class Subject_Assign(models.Model): # 팀 테이블
    user_num = models.IntegerField(null = True)
    subject_num = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)

    def str(self):
        return self.num

class Team(models.Model): # 팀 테이블
    num = models.AutoField(primary_key=True)                        # 팀 번호(주키)
    created_date = models.DateTimeField(default=timezone.now)       # 팀 생성 날짜
    team_name = models.CharField(max_length=100)                    # 팀 이름
    project_name = models.CharField(max_length=100)                 # 프로젝트 이름
    text = models.TextField()                                       # 프로젝트 내용
    doc_link = models.CharField(max_length=100, null=True)          # 공유문서 링크
    subject_num = models.IntegerField(null = True)

    def str(self):
        return self.num

class User_extends(models.Model): # 유저 테이블 (auth_user 테이블을 OneToOne 방식으로 확장,팀 번호 속성을 부여하기 위해 확장함)
    user = models.OneToOneField(User, on_delete=models.CASCADE) #auth_user와 One to One 세팅
    team_num = models.ForeignKey(Team, on_delete=models.CASCADE, null=True) #팀 번호 속성

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        User_extends.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.user_extends.save()
#sender=User 설정에 의해서 User의 save() 가 호출될 때마다 그 직후에 create_user_profile, save_user_profile 이 호출된다.

class FileListBox(models.Model): # 파일 리스트 테이블
    file_name = models.TextField(max_length=255, blank=False) # 파일 이름
    uploaded_date = models.DateTimeField(auto_now_add=False,default=timezone.now) # 업로드된, 수정된 날짜
    team_title = models.CharField(max_length=20, blank=False) # 팀 이름
    file_size = models.FloatField(null=True, blank=True, default=0) # 파일 크기
    document = models.FileField(upload_to='documents/',max_length=1500) # 파일 업로드 field
    t_num = models.IntegerField(default=0,blank=False) # 팀 그룹 아이디 넘버

class Message(models.Model):
    author = models.ForeignKey(get_user_model(), related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    roomName = models.TextField()

    def __str__(self):
        return self.author.username

    def last_10_messages(room):
        return Message.objects.order_by('timestamp').filter(roomName=room)