import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Disciplina

class SearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        response = text_data_json.get('q', '')
        search_where = text_data_json.get('w', '')

        if response and len(response) > 2:
            #Per risolvere il problema dell'asincronia
            def get_suggestion():
                if search_where == 'nome':
                    q = Disciplina.objects.filter(nome__icontains=response).first()
                    if q:
                        return q.nome
                    else:
                        return ""
                else:
                    q = Disciplina.objects.filter(personal_trainer__username__icontains=response).first()
                    if q:
                        return q.personal_trainer.username
                    else:
                        return ""

            suggestion = await sync_to_async(get_suggestion)()
            
            if suggestion != "":
                response = suggestion
            
        await self.send(text_data=json.dumps({
            'response': response
        }))