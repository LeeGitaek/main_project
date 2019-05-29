
#base.html에 유저가 수강하고있는 과목 객체들을 항상 넘겨준다. 따로 view를 호출하지 않아도 됨 이를 contetxt processor라고 한다. setting에 TEMPLATE에 설정되어있음.

from .models import Subject_Assign

def default(request):
    qs = Subject_Assign.objects.all()
    return dict(
        subjects_ = qs,
    )
