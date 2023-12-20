import secrets
import base64
import json
from asgiref.sync import async_to_sync
from django.core.cache import cache
from django.contrib.auth.models import User
from channels.layers import get_channel_layer

from apps.chat.models import Messages as MessagesModel
from apps.chat.serializers import MessageSerializer
from .message_props import HandleUser, HandleHomePage, HandleMessage, HandleFile, HandleImage
from .exceptions import MessageException


class Message:
    key_len = 6
    key_prefix = "msg_"
    cash_time = 3600
    user = HandleUser()
    homepage = HandleHomePage()
    message = HandleMessage()
    file = HandleFile()
    image = HandleImage()

    def __init__(self, user=None, **kwargs):
        self._user = None
        self._file = None
        self._image = None
        self.data = {
            "parent": kwargs.get('parent'),
            "username": kwargs.get('username'),
            "email": kwargs.get('email'),
            "homepage": kwargs.get('homepage'),
            "message": kwargs.get('message'),
            "file_name": kwargs.get("file_name"),
            "file_data": kwargs.get("file_data"),
            "image_name": kwargs.get("image_name"),
            "image_data": kwargs.get("image_data"),
        }
        self.user = user

    def save_to_cache(self):
        data = {
            "parent": self.parent.id if self.parent else None,
            "username": self.user.username if self.user else self.data.get("username"),
            "email": self.user.email if self.user else self.data.get("email"),
            "homepage": self.homepage,
            "message": self.message,
            "file_name": self.file.name if self.file else None,
            "file_data": base64.b64encode(self.file.file.getvalue()).decode("utf-8") if self.file else None,
            "image_name": self.image.name if self.image else None,
            "image_data": base64.b64encode(self.image.file.getvalue()).decode("utf-8") if self.image else None,
        }
        key = secrets.token_urlsafe(self.key_len)
        cache.set(f"{self.key_prefix}{key}", json.dumps(data), self.cash_time)
        return key

    def save_to_db(self):
        if not self.user:
            user = User.objects.create_user(
                username=self.data.get("username"),
                email=self.data.get("email")
            )
            user.save()
            self.user = user

        message = MessagesModel(
            user=self.user,
            parent=self.parent,
            homepage=self.homepage,
            message=self.message,
            file=self.file,
            image=self.image
        )
        message.save()

        self._sand_message_to_grope(msg=message)

    def confirm(self, key):
        data = cache.get(f"{self.key_prefix}{key}", None)
        if not data:
            raise MessageException("Wrong key")
        self.data = json.loads(data)
        self.save_to_db()
        cache.delete(f"{self.key_prefix}{key}")
        return self.user

    @staticmethod
    def _sand_message_to_grope(msg):
        data = MessageSerializer(msg).data
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)("main_chat", {"type": "chat_message", "message": data})

    @property
    def parent(self):
        parent_id = self.data.get("parent")
        if not parent_id:
            return None

        parent = MessagesModel.objects.filter(id=parent_id)
        if not parent.count():
            raise MessageException(f"Message id={parent_id} doesn't exist.")

        return parent.get()
