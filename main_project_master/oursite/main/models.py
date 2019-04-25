from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
## DEVELOPER : 이기택
## BOX APP
## Box 박스 앱 MODELS CODE START ##
## 2019/04/21 21:22 MOVED ##
# box model import -- start #

# box model import -- end #
## Box 박스 앱 MODELS CODE END ##
## DEVELOPER : 이기택
## BOX APP
## 2019/04/21 21:22 MOVED ##

# 팀 모델
class Team(models.Model):
    num = models.AutoField(primary_key=True)                        # 팀 번호(주키)
    created_date = models.DateTimeField(default=timezone.now)       # 팀 생성 날짜
    team_name = models.CharField(max_length=100)                    # 팀 이름
    project_name = models.CharField(max_length=100)                 # 프로젝트 이름
    text = models.TextField()                                       # 프로젝트 내용
    doc_link = models.CharField(max_length=100, null=True)          # 공유문서 링크
    subject_num = models.IntegerField(null = True)

    def str(self):
        return self.num

# 과목 모델
class Subject(models.Model):
    num = models.AutoField(primary_key=True)                        # 과목 번호(주키)
    created_date = models.DateTimeField(default=timezone.now)       # 과목 생성 날짜
    subject_name = models.CharField(max_length=100)                    # 과목 이름
    team_num = models.ForeignKey(Team, on_delete=models.CASCADE) #팀 테이블을 참조하는 외래키
    userid = models.CharField(max_length=50,blank=False,default='DEFAULT VALUE')   #유저아이디 키

    def str(self):
        return self.num

# 유저 모델 (auth_user 테이블을 OneToOne 방식으로 확장,팀 번호 속성을 부여하기 위해 확장함)
class UserTeam(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #auth_user와 One to One 세팅
    team_num = models.ForeignKey(Team, on_delete=models.CASCADE, null=True) #팀 번호 속성

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserTeam.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userteam.save()

#sender=User 설정에 의해서 User의 save() 가 호출될 때마다 그 직후에 create_user_profile, save_user_profile 이 호출된다.

## DEVELOPER : 이기택
## BOX APP
## Box 박스 앱 MODELS CODE START ##
## 2019/04/21 21:22 MOVED ##

# box model code -- start #

class FileListBox(models.Model): # 파일 리스트 테이블
    file_name = models.TextField(max_length=255, blank=False)  # 파일 이름
    class_name = models.CharField(max_length=20, blank=False) # 수업 이름
    uploaded_date = models.DateTimeField(auto_now_add=False,default=timezone.now) # 업로드된, 수정된 날짜
    team_title = models.CharField(max_length=20, blank=False) # 팀 이름
    user_name = models.CharField(max_length=10, blank=False) # 유저의 이름
    weights_num = models.FloatField(null=True, blank=True, default=1200.00) # 인공지능에 쓰일 가중치 값 기본 값은 0이다.
    assignment_title = models.CharField(max_length=20, blank=True) # 과제 이름
    deadline_date = models.DateTimeField(auto_now_add=False,default=timezone.now) # 데드라인 날짜 (인공지능에 쓰일 변수값)
    file_size = models.FloatField(null=True, blank=True, default=0) # 파일 크기
    #document_similarity = models.FloatField(null=True, blank=True, default=0) # 내용 파일 유사도 점수 float 값이다.
    #reward_score = models.FloatField(null=True, blank=True, default=0) # 인공지능에 쓰일 강화학습용 보상점수이다.
    document = models.FileField(upload_to='documents/',max_length=1500) # 파일 업로드 field
    t_num = models.IntegerField(default=0,blank=False) # 팀 그룹 아이디 넘버

class NotificationBox(models.Model): # 알림 테이블
    uploaded_filename = models.TextField(max_length=255, blank=False) # 업로드 된 파일 이름
    uploaded_account = models.CharField(max_length=10, blank=False) # 업로드한 계정 이름
    uploaded_datetime = models.DateTimeField(auto_now_add=False,default=timezone.now) # 업로드 날짜 , 시간
    uploaded_teamtitle = models.CharField(max_length=20, blank=False) # 팀 이름
    edited_orwhat =  models.BooleanField(default=False) # 수정 여부
    read_ox = models.BooleanField(default=False) # 알림을 사용자가 읽었는지 여부
    uploaded_groupid = models.IntegerField(default=0,blank=False) # 팀 그룹 아이디 넘버

class InviteBox(models.Model):
    sender = models.CharField(max_length=10, blank=False) # 초대를 보낸 사람 이름
    receiver = models.CharField(max_length=10, blank=False) # 초대를 받은 사람 이름
    class_name = models.CharField(max_length=20, blank=False) # 수업 이름

class TaskBox(models.Model): # task  테이블
    task_user = models.CharField(max_length=20, blank=False) # 사용자
    task_role = models.CharField(max_length=10, blank=False) # 역할
    task_status = models.CharField(max_length=10, blank=False) # 상태
    task_percent = models.IntegerField(default=0,blank=False) # 진행상황
    task_dead = models.CharField(max_length=20, blank=False)  # 데드라인
    task_subject = models.CharField(max_length=20, blank=False) # 과목
    task_team =  models.IntegerField(default=0,blank=False) # 팀 그룹 아이디 넘버

class RoleCredit(models.Model):  # 크레딧 시스템 테이블
    credit_role =  models.CharField(max_length=10, blank=False) #역할
    credit_per = models.FloatField(null=True, blank=True, default=0.1) # 크레딧 가중치

class DeadCredit(models.Model): # 크레딧 시스템 테이블
    credit_dead = models.DateTimeField(auto_now_add=False) # 데드라인
    credit_per_two = models.FloatField(null=True, blank=True, default=0.3) #크레딧 가중치

class ReviewBox(models.Model): #파일 평가 테이블
    review_file = models.CharField(max_length=255, blank=False) # 파일이름
    review_uploader = models.CharField(max_length=10, blank=False) # 업로더
    review_subject = models.CharField(max_length=20, blank=False) # 과목
    review_team = models.IntegerField(default=0,blank=False) # 팀 그룹 아이디 넘버
    review_er = models.CharField(max_length=20, blank=False) # 평가자
    review_score = models.FloatField(default=0.0,blank=False) # 평가점수
    review_comments = models.CharField(max_length=255, blank=True, default="의견 없음") # 평가 피드백 댓글 ,의견
    review_date =  models.DateTimeField(auto_now_add=False,default=timezone.now) #평가 날짜

class ReviewCredit(models.Model):  # 크레딧 시스템 테이블
    credit_review_score = models.IntegerField(default=0,blank=False) # 리뷰 점수
    credit_per_three =  models.FloatField(null=True, blank=True, default=0.35) # 크레딧 가중치

class TeamHistoryCredit(models.Model): # 협업 히스토리 크레딧 시스템 테이블
    th_user = models.CharField(max_length=20, blank=False) # 사용자
    th_count_of_history = models.FloatField(null=True, blank=True, default=0.0) # 협업 히스토리 카운트
    th_credit = models.FloatField(null=True, blank=True, default=0.15) # 크레딧 가중치


# box model code -- end #
## Box 박스 앱 MODELS CODE END ##
## DEVELOPER : 이기택
## BOX APP
## 2019/04/21 21:22 MOVED ##
