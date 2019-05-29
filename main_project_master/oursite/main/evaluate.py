import math

from .models import Message
from google.cloud import language_v1
from google.cloud.language_v1 import enums
import six

class Evaluate():

    def evalMessage(self, username, room):
        myMessage = Message.objects.order_by('timestamp').filter(author_id=username).filter(roomName=room)
        allMessage = Message.objects.order_by('timestamp').filter(roomName=room)

        eva_percent = round((len(myMessage) / len(allMessage) * 100), 2)
        talkTime = 0
        content = ''

        for idx, data in enumerate(myMessage):
            print(idx)
            print(data.content)
            now = data.timestamp
            if idx != 0 :
                content += data.content
                talkTime += (now - pre).seconds
            pre = data.timestamp

        try:
            eva_talkTime = talkTime / (len(myMessage)-1)
        except :
            eva_talkTime = talkTime

        eva_content = content / len(myMessage)

        client = language_v1.LanguageServiceClient.from_service_account_json("..\static\dist\MyFirstProject-2dec78b0b71b.json")
        if isinstance(content, six.binary_type):
            content = content.decode('utf-8')

        type_ = enums.Document.Type.PLAIN_TEXT
        document = {'type': type_, 'content': content}

        response = client.analyze_sentiment(document)
        sentiment = response.document_sentiment
        eva_sentiment = sentiment.score

        # Meeting_Evaluate.objects.creat(team_num=team_pk, meeting_num=meeting_num, user_from=user_pk, )
