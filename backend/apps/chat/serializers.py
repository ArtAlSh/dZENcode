import json
import secrets
from django.conf import settings
from django.core.cache import cache
from rest_framework import serializers
from .models import Messages

from django.contrib.auth.models import User


class MessageSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(source="user", slug_field="username", queryset=User.objects.all())
    email = serializers.SlugRelatedField(source="user", slug_field="email", queryset=User.objects.all())
    comments_num = serializers.SerializerMethodField()

    class Meta:
        model = Messages
        fields = ["id", "username", "email", "parent", "homepage", "message", "file", "image", "date", "comments_num"]
        read_only_fields = ["date"]

    def get_comments_num(self, obj):
        return obj.messages.count()
