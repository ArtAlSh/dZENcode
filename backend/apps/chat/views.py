import django_filters.rest_framework
from rest_framework.generics import ListAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import MessageSerializer
from .models import Messages
from .filters import MessageFilter
from .utils import Message, MessageException, send_confirmation_code


class MessagesView(ListAPIView):
    serializer_class = MessageSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_class = MessageFilter

    def post(self, request: Request, *args, **kwargs):
        try:
            if request.auth:
                message = Message(user=request.user, **request.data)
                message.save_to_db()
                response = {
                    "result": "Message was saved.",
                    "requires_confirmation": False
                }
            else:
                message = Message(**request.data)
                key = message.save_to_cache()
                send_confirmation_code(key, message.data.get("email"))
                response = {
                    "result": "Message needs confirmation.",
                    "requires_confirmation": True
                }
        except MessageException as me:
            return Response({"result": str(me), "requires_confirmation": False}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"result": "Internal error.", "requires_confirmation": False}, status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs):
        auth = None
        try:
            key = request.data.get("key")
            message = Message()
            user = message.confirm(key)
            refresh = RefreshToken.for_user(user)
            auth = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "username": user.username,
                "email": user.email,
            }
        except MessageException as me:
            return Response({"result": str(me), "auth": None}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"result": "Internal error.", "auth": None}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"result": "Success", "auth": auth}, status=status.HTTP_201_CREATED)

    def get_queryset(self):
        if parent := self.kwargs.get("parent"):
            return Messages.objects.filter(parent=parent)
        else:
            return Messages.objects.filter(parent__isnull=True)
