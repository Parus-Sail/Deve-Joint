import json

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from project_app.models import Project

from .models import Chat


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['project_id']
        self.room_group_name = f'chat_{self.id}'
        # join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        now = timezone.now()

        # accept connection
        await self.accept()
        messages = await self.load_messages_from_db(project_id=self.id)

        for message in messages:
            event = {
                'type': 'chat_message',
                'message': message['message'],
                'user': message['author__username'],
                'datetime': now.isoformat(),
            }

            await self.send(json.dumps(event))

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        now = timezone.now()

        # Сохранение сообщения в базе данных (пример для асинхронного режима)
        await self.save_message_to_db(
            project_id=self.id,
            user=self.user,
            message=message,
        )

        # send message to room group
        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': message,
            'user': self.user.username,
            'datetime': now.isoformat(),
        })

    # receive message from room group
    async def chat_message(self, event):
        # send message to WebSocket
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def save_message_to_db(self, project_id: int, user, message: str):
        project = Project.objects.get(id=project_id)
        return Chat.objects.create(author=user, project=project, message=message)

    @database_sync_to_async
    def load_messages_from_db(self, project_id: int):
        messages = Chat.objects.filter(project=project_id).values('message', 'author__username', 'time')[:3][::-1]
        return list(messages)
