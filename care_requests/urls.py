from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_request, name='create_request'),
    path('my/', views.my_requests, name='my_requests'),
    path('<int:pk>/', views.request_detail, name='request_detail'),
    path('edit/<int:pk>/', views.edit_request, name='edit_request'),
    path('delete/<int:pk>/', views.delete_request, name='delete_request'),
]
