from django.urls import path
from . import views

urlpatterns = [
    path("", views.MessagesView.as_view()),
    path("<str:parent>/", views.MessagesView.as_view()),
]
