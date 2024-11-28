from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer

class NotificationSystem(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        self.group_name = self.scope['url_route']['kwargs']['group']
        await self.channel_layer.group_add(self.group_name,self.channel_name)

    async def receive(self, text_data=None, bytes_data=None):
        await self.channel_layer.group_send(self.group_name,{
            'type':'send.message',
            'message':text_data
        })

    async def send_message(self, event):
        await self.send(text_data=event.get('message'))
    
    async def disconnect(self, event):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        raise StopConsumer()