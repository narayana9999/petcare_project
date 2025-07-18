from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')  
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


@csrf_protect
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()   
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('dashboard')  



from pets.models import Pet
from care_requests.models import CareRequest, Application
from message.models import Message

@login_required
def dashboard(request):
    user = request.user
    context = {}

    if user.is_owner:
        context['pets'] = Pet.objects.filter(owner=user)
        context['my_requests'] = CareRequest.objects.filter(owner=user)
        context['received_applications'] = Application.objects.filter(care_request__owner=user)

    if user.is_sitter:
        assigned_request_ids = Application.objects.filter(status='Accepted').values_list('care_request_id', flat=True)
        context['available_requests'] = CareRequest.objects.filter(is_fulfilled=False).exclude(
            Q(owner=user) | Q(id__in=assigned_request_ids)
            )
        context['my_applications'] = Application.objects.filter(sitter=user)
        context['assigned_requests'] = Application.objects.filter(sitter=user, status='Accepted')

    return render(request, 'accounts/dashboard.html', context)

from .forms import CustomUserCreationForm
from django.contrib.auth import login

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


from .forms import UserProfileForm
from django.contrib import messages

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user_obj': request.user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile_view')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'accounts/profile_edit.html', {'form': form})


from django.shortcuts import render, get_object_or_404
from .models import User
from pets.models import Pet
from care_requests.models import Application

def public_profile(request, user_id):
    user_obj = get_object_or_404(User, id=user_id)
    pets = Pet.objects.filter(owner=user_obj) if user_obj.is_owner else None
    

    context = {
        'user_obj': user_obj,
        'pets': pets,
         
    }
    return render(request, 'accounts/public_profile.html', context)

from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

@login_required
def leave_review(request, sitter_id):
    sitter = get_object_or_404(User, id=sitter_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = request.user
            review.sitter = sitter
            review.save()
            return redirect('public_profile', user_id=sitter.id)
    else:
        form = ReviewForm()

    return render(request, 'accounts/leave_review.html', {'form': form, 'sitter': sitter})
