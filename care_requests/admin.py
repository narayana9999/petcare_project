from django.contrib import admin
from .models import CareRequest, Application

@admin.register(CareRequest)
class CareRequestAdmin(admin.ModelAdmin):
    list_display = ['pet', 'owner', 'start_date', 'end_date', 'is_fulfilled']
    list_filter = ['is_fulfilled']
    search_fields = ['pet__name', 'owner__username']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['care_request', 'sitter', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['sitter__username']
