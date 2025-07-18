from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

urlpatterns += [
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit, name='profile_edit'),
]

urlpatterns += [
    path('user/<int:user_id>/', views.public_profile, name='public_profile'),
    path('review/<int:sitter_id>/', views.leave_review, name='leave_review'),
    path('profile/<int:user_id>/', views.public_profile, name='public_profile'),

]
