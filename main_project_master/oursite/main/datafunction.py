
from main.models import User,FileListBox,Message,Meeting_Evaluate,Meeting,Subject_Assign,Subject,Team
from django.http import Http404
from django.contrib.auth.models import User as AuthUser
from django.core.files.storage import FileSystemStorage 
import datetime
import difflib

def addShare(username,teamnum,teamname,files):
	now=datetime.datetime.now()
	formatted_date=now.strftime('%Y-%m-%d %H:%M:%S')
	fs = FileSystemStorage()
	user = User.objects.filter(username__iexact=username).first()

	if user is None:
		raise Http404('User does not exist')

	for f in files:
		FileListBox.objects.create(file_name=f.name, team_title=teamname,file_size=f.size, document=fs.url(f.name) ,t_num = teamnum ,uploaded_date=formatted_date)





