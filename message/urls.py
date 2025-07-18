from django.urls import path
from . import views

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('chat/<int:user_id>/', views.chat_view, name='chat_view'),
    path('send/', views.send_message, name='send_message'),
]
