from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model

class Team(models.Model): # 팀 테이블
    num = models.AutoField(primary_key=True)                        # 팀 번호(주키)
    created_date = models.DateTimeField(default=timezone.now)       # 팀 생성 날짜
    team_name = models.CharField(max_length=100)                    # 팀 이름
    project_name = models.CharField(max_length=100)                 # 프로젝트 이름
    text = models.TextField()                                       # 프로젝트 내용
    subject_num = models.IntegerField(null = True)
    hash = models.CharField(max_length=100)

    def str(self):
        return self.num
#게시물 종류
# 1=(notice, 공지) / 2=(assighnment, 과제) / 3=(debate, 토론)
class PostType(models.Model):
    en_name = models.CharField(max_length=50) # en_name(url에 포함시킬 영어 이름)
    kr_name = models.CharField(max_length=50) # kr_name(템플릿에 보여줄 한글 이름

    def __str__(self):
        return self.en_name

# 게시물
class Post(models.Model):
    subject = models.ForeignKey('main.Subject', related_name='posts', on_delete=models.CASCADE) # 과목 확인
    post_type = models.ForeignKey('main.PostType', on_delete=models.CASCADE) # 게시판 타입 확인
    auth = models.ForeignKey("auth.User", on_delete=models.CASCADE) # 작성자 확인
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add = True) # 생성 당시의 시간을 그대로 저장해준다
    visit = models.PositiveIntegerField(default = 0)
    documents = models.FileField(null=True,upload_to='documents/',max_length=1500)
    file_name = models.TextField(null=True,max_length=255, blank=False) # 파일 이름

    def __str__(self):
        return "< {num} - {title} >".format(num=self.post_type.pk, title=self.title)

    def counter_visit(self):
        self.visit += 1
        self.save()

# 댓글
class Comment(models.Model):
    post = models.ForeignKey('main.Post', related_name='comments', on_delete=models.CASCADE)
    auth = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    created_date=models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['-id']

class Subject(models.Model):
    num = models.IntegerField(primary_key=True)  # 과목 번호(주키)
    subject_name = models.CharField(max_length=100)  # 과목 이름
    prof = models.CharField(max_length=50)  # 교수님 성함
    created_date = models.DateTimeField(auto_now_add=True)
    auth = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    def __str__(self):
        return "< {num} - {prof} - {name} >".format(num=self.num, name=self.subject_name, prof=self.prof)

class Subject_Assign(models.Model): #유저, 과목 관계 테이블
    user_num = models.IntegerField(null=True)
    subject_num = models.ForeignKey(Subject, on_delete=models.CASCADE, null=True)
    team_num = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    evaluate = models.FloatField(default=0)

    def str(self):
        return self.num

class Meeting(models.Model):
    team_num = models.ForeignKey(Team, on_delete=models.CASCADE)
    meeting_num = models.IntegerField()
    date_start = models.DateTimeField() #회의 시작 시간
    date_end = models.DateTimeField() #회의 종료 시간
    title = models.CharField(max_length=200) #회의제목
    hash = models.CharField(max_length=100)


class Meeting_Evaluate(models.Model):
    team_num = models.IntegerField()
    meeting_num = models.IntegerField()
    user_from = models.IntegerField()
    user_num = models.IntegerField()
    evaluate = models.FloatField(default=0)

'''
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
'''

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
