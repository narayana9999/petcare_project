from django.shortcuts import render
from .models import Guide

def guide_list(request):
    guides = Guide.objects.all()
    return render(request, 'care_guides/list.html', {'guides': guides})
