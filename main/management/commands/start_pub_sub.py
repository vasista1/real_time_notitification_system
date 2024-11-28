from django.core.management.base import BaseCommand
import redis

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer



class Command(BaseCommand):

    help = '''Starts Pub Sub (Subscriber) that listens for any messages from Publisher 
    and sends that message to group(channel)'''

    def handle(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        redis_client = redis.Redis(host='127.0.0.1',port=6379)
        pub_sub = redis_client.pubsub()
        pub_sub.subscribe('notification_system')

        self.stdout.write(self.style.SUCCESS("Subscribed to Redis channel 'notification_system'"))

        for message in pub_sub.listen():
            if message['type'] ==  'message':
                async_to_sync(channel_layer.group_send)('notification_system',{
                    'type':'send.message',
                    'message': message.get('data').decode('utf-8')
                })