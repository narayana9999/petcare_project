from django.contrib import admin
from .models import Guide

@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ['title', 'pet_type', 'author', 'created_at']
    search_fields = ['title', 'pet_type']
