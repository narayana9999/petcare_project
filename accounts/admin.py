from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['username', 'email', 'is_owner', 'is_sitter', 'location']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_owner', 'is_sitter', 'bio', 'phone_number', 'profile_picture', 'location')}),
    )

from .models import Review
admin.site.register(Review)
