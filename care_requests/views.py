from django.shortcuts import render, redirect, get_object_or_404
from .forms import CareRequestForm, ApplicationForm
from .models import CareRequest, Application
from pets.models import Pet
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST


@login_required
def create_request(request):
    if request.method == 'POST':
        form = CareRequestForm(request.POST, user=request.user)
        if form.is_valid():
            care_request = form.save(commit=False)
            care_request.owner = request.user
            care_request.save()
            return redirect('dashboard')
    else:
        form = CareRequestForm(user=request.user)

    return render(request, 'care_requests/care_request.html', {'form': form})


@login_required
def my_requests(request):
    requests = CareRequest.objects.filter(owner=request.user)
    return render(request, 'care_requests/my_requests.html', {'requests': requests})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CareRequest, Application

@login_required
def request_detail(request, pk):
    care_request = get_object_or_404(CareRequest, pk=pk)
    applications = None
    existing_application = None

    # Load applications if user is the owner
    if request.user == care_request.owner:
        applications = Application.objects.filter(care_request=care_request)

    # Load sitter's existing application if applicable
    if request.user.is_sitter:
        existing_application = Application.objects.filter(
            care_request=care_request,
            sitter=request.user
        ).first()

    # Handle form submissions
    if request.method == 'POST':
        action = request.POST.get('action')

        # Owner updating application status
        if request.user == care_request.owner and action == 'update_status':
            app_id = request.POST.get('application_id')
            new_status = request.POST.get('status')

            if app_id and new_status in ['Pending', 'Accepted', 'Rejected']:
                try:
                    app = Application.objects.get(id=app_id, care_request=care_request)
                    app.status = new_status
                    app.save()
                    messages.success(request, f"Status updated to {new_status}.")
                    return redirect('request_detail', pk=care_request.pk)
                except Application.DoesNotExist:
                    messages.error(request, "Application not found.")

        # Sitter submitting a new application
        elif request.user.is_sitter and action == 'apply_now':
            if not existing_application:
                Application.objects.create(
                    care_request=care_request,
                    sitter=request.user,
                    status='Pending'
                )
                messages.success(request, 'You have applied successfully.')
                return redirect('dashboard')

    return render(request, 'care_requests/care_request_detail.html', {
        'care_request': care_request,
        'applications': applications,
        'existing_application': existing_application,
    })

@login_required
def edit_request(request, pk):
    care_request = get_object_or_404(CareRequest, pk=pk, owner=request.user)
    form = CareRequestForm(request.POST or None, instance=care_request, user=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, "Care request updated.")
        return redirect('dashboard')
    return render(request, 'care_requests/edit_request.html', {'form': form})

@login_required
def delete_request(request, pk):
    care_request = get_object_or_404(CareRequest, pk=pk, owner=request.user)
    if request.method == 'POST':
        care_request.delete()
        messages.success(request, "Care request deleted.")
        return redirect('dashboard')
    return render(request, 'care_requests/delete_request.html', {'request_obj': care_request})
