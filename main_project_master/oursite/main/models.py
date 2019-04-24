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



class Transactions(models.Model):
    sender = models.CharField(max_length=200)
    receiver = models.CharField(max_length=200)
    amount = models.IntegerField(default =0)
    time_stamp = models.DateTimeField(auto_now_add=True)
    added_to_block = models.BooleanField(default=False)

    def __str__(self):
        return "'%s' 전송됨 '%d' 크레딧 '%s' 에게" % (self.sender, self.amount, self.receiver, )


from faker import Faker
rand = Faker()


class Block(models.Model):
    time_stamp = models.DateTimeField(auto_now_add=False)
    index = models.IntegerField(auto_created=True, blank=True)
    data = models.TextField(blank=True, max_length=255)
    hash = models.CharField(max_length=255, blank=True)
    previous_hash = models.CharField(max_length=255)
    chain = models.ForeignKey(to='Chain', on_delete=models.CASCADE)
    nonce = models.CharField(max_length=255, default=0, blank=True)

    def __str__(self):
        return "Block " + str(self.index) + " on " + self.chain.name

    def __repr__(self):
        return '{}: {}'.format(self.index, str(self.hash)[:6])

    def __hash__(self):
        return sha256(
            u'{}{}{}{}'.format(
                self.index,
                self.data,
                self.previous_hash,
                self.nonce).encode('utf-8')).hexdigest()

    @staticmethod
    def generate_next(latest_block, data):
        block = Block(
            data=data,
            index=latest_block.index + 1,
            time_stamp=datetime.datetime.now(tz=pytz.utc),
            previous_hash=latest_block.hash,
            nonce=SymmetricEncryption.generate_salt(26),
        )
        while not block.valid_hash():
            block.nonce = SymmetricEncryption.generate_salt(26)
        block.hash = block.__hash__()

        # block.save()                # todo: remove

        return block

    def is_valid_block(self, previous_block):
        if self.index != previous_block.index + 1:
            log.warning('%s: Invalid index: %s and %s' % (self.index, self.index, previous_block.index))
            return False
        if self.previous_hash != previous_block.hash:
            log.warning('%s: Invalid previous hash: %s and %s' % (self.index, self.hash, previous_block.hash))
            return False

        if self.__hash__() != self.hash and self.index > 1:
            log.warning('%s: Invalid hash of content: %s and %s' % (self.index, self.hash, self.__hash__()))
            return False
        if not self.valid_hash() and self.index > 1:
            log.warning('%s: Invalid hash value: %s' % (self.index, self.hash))
            return False
        return True

    def valid_hash(self):
        """블록체인 Proof of work 합의 증명 알고리즘"""
        return self.__hash__()[:4] == '0000'


class Chain(models.Model):
    """
    동시에 여러개의 블록체인 요소들 승인
    """
    time_stamp = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def __len__(self):
        return self.block_set.count()

    def __repr__(self):
        return '{}: {}'.format(self.name, self.last_block)

    @property
    def last_block(self):
        return self.block_set.order_by('index').last()

    def create_seed(self):
        assert self.pk is not None
        seed = Block.generate_next(
            Block(hash=sha256('seed'.encode('utf-8')).hexdigest(),
                  index=-1),
            data='Seed data',
        )
        seed.chain = self
        seed.save()

    def is_valid_next_block(self, block):
        return block.is_valid_block(self.last_block)

    def add(self, data):
        if not self.block_set.count():
            self.create_seed()

        block = Block.generate_next(
            self.last_block,
            data
        )
        block.chain = self
        return block

    def is_valid_chain(self, blocks=None):
        blocks = blocks or list(self.block_set.order_by('index'))
        if not len(blocks):
            log.warning('체인이 없습니다.')
            return False
        if len(blocks) == 1 and blocks[0].index != 0:
            log.warning('Missing seed block in chain.')
            return False
        if not all(pblock.index + 1 == block.index == required_index
                   for pblock, block, required_index in zip(blocks[:-1], blocks[1:], range(1, len(blocks)))):
            log.warning('Chain is not sequential')
            return False
        return all(block.is_valid_block(pblock)
                   for pblock, block in zip(blocks[:-1], blocks[1:]))

    def replace_chain(self, new_chain):
        if self.is_valid_chain(new_chain) and len(new_chain) > len(self):
            self.block_set.all().delete()
            for block in new_chain:
                block.chain = self
                block.save()



class Peer(models.Model): # 블록체인 개발 노드 피어 투 피어 클래스
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name + "@" + self.address

    def __repr__(self):
        return '{}: {}'.format(self.name, self.address)

    def broadcast(self, chain_name, block):
        from .api.v0.serializers import BlockSerializer
        block_data = BlockSerializer(data=block.__dict__).as_json()
        for peer in Peer.objects.order_by('-id'):
            # import pdb
            # pdb.set_trace()
            print("보냅니다", peer)
            JsonApi.post(
                         peer.address,
                         reverse('mine-block',
                                 kwargs={'chain_name': chain_name}),
                         data=block_data)

    def query_latest_block(self, chain_name):
        from .api.v0.serializers import BlockSerializer
        data = JsonApi.get(self.address,
                           reverse('latest-block',
                                   kwargs={'chain_name': chain_name}))
        serializer = BlockSerializer(data=data)
        serializer.is_valid()
        instance = Block(**serializer.validated_data)
        instance.chain = Chain.objects.get(name=chain_name)
        return instance

    def query_chain(self, chain_name):
        from .api.v0.serializers import BlockSerializer
        chain = Chain.objects.get(name=chain_name)
        data = JsonApi.get(self.address,
                           reverse('chain',
                                   kwargs={'name': chain_name}))

        blocks = []
        for block_data in data.get('block_set', []):
            serializer = BlockSerializer(data=block_data)
            if serializer.is_valid():
                block = Block(**serializer.validated_data)
                block.chain = chain
                blocks.append(block)

        return blocks

    def fetch_longest_chain(self, chain_name):
        chain = max(
            (peer.query_chain(chain_name)
             for peer in self.discover_all_peers()),
            key=len
        )
        return sorted(chain, key=lambda x: x.index)

    def mine_block(self, chain_name, data, password=None):
        chain = Chain.objects.get(name=chain_name)
        if password is not None:
            data = EncryptionApi.encrypt(password, data)
        new_block = chain.add(data)
        self.broadcast(chain_name, new_block)

    def synchronize(self, chain_name):
        self.discover_all_peers(commit=True)
        chain = Chain.objects.get(name=chain_name)
        longest_chain = self.fetch_longest_chain(chain_name)
        chain.replace_chain(longest_chain)

    def query_peers(self):
        from .api.v0.serializers import PeerSerializer
        data = JsonApi.get(self.address,
                           reverse('peers'))

        peers = []
        for peer in data:
            serializer = PeerSerializer(data=peer)
            if serializer.is_valid():
                peers.append(Peer(**serializer.validated_data))

        return peers

    @classmethod
    def scan_peers(cls, peers, known_peers):
        known_peers = set(p.address for p in known_peers)
        new_peers = []
        for peer in peers:
            foreign_peers = peer.query_peers()
            for fp in foreign_peers:
                if fp.address not in known_peers:
                    new_peers.append(fp)

        return new_peers

    @classmethod
    def discover_all_peers(cls, commit=False):
        discoveries = Peer.objects.all()
        known_peers = []
        while len(discoveries):
            known_peers.extend(discoveries)
            discoveries = cls.scan_peers(discoveries, known_peers)

        if commit:
            for peer in known_peers:
                peer.save()

        return known_peers

# box model code -- end #
## Box 박스 앱 MODELS CODE END ##
## DEVELOPER : 이기택
## BOX APP
## 2019/04/21 21:22 MOVED ##
