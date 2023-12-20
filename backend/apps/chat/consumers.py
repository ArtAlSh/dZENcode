from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels_redis.core import RedisChannelLayer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    main_chat_name = "main_chat"

    async def connect(self):
        print(f"Connected: {self.channel_name}")
        self.channel_layer: RedisChannelLayer
        await self.channel_layer.group_add(self.main_chat_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        print(f"Disconnected: {self.channel_name}")
        self.channel_layer: RedisChannelLayer
        await self.channel_layer.group_discard(self.main_chat_name, self.channel_name)

    async def chat_message(self, event):
        message = event["message"]
        print(f"Send to groupe: {message}")
        await self.send_json(message)
