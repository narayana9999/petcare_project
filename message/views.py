from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from accounts.models import User
from .models import Message

@login_required
def inbox(request):
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'message/inbox.html', {'users': users})

@login_required
def chat_view(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    messages = Message.objects.filter(
        sender__in=[request.user, target_user],
        receiver__in=[request.user, target_user]
    )
    return render(request, 'message/chat.html', {
        'target_user': target_user,
        'messages': messages,
    })

@login_required
def send_message(request):
    if request.method == 'POST':
        sender = request.user
        receiver_id = request.POST.get('receiver_id')
        content = request.POST.get('content')

        if content and receiver_id:
            receiver = get_object_or_404(User, id=receiver_id)
            Message.objects.create(sender=sender, receiver=receiver, content=content)
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'}, status=400)
