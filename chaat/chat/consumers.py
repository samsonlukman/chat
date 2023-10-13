import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import ChatMessage

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)
        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope['user']

        # Save the chat message to the database
        chat_message = ChatMessage.objects.create(user=user, message=message)

        async_to_sync(self.channel_layer.group_send)(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'user': user.username,  # Include the username
            'timestamp': chat_message.timestamp.strftime('%Y-%m-%d %H:%M:%S')  # Include the timestamp
        })

    def chat_message(self, event):
        message = event['message']
        user = event['user']  # Extract the username
        timestamp = event['timestamp']  # Extract the timestamp

        self.send(text_data=json.dumps({
            'type': 'chat',
            'message': message,
            'user': user,
            'timestamp': timestamp
        }))
