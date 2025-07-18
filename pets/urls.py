from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_pet, name='add_pet'),
    path('my/', views.my_pets, name='my_pets'),
    path('edit/<int:pk>/', views.edit_pet, name='edit_pet'),
    path('delete/<int:pk>/', views.delete_pet, name='delete_pet'),
    path('pet/<int:pet_id>/', views.pet_detail, name='pet_detail'),

]
