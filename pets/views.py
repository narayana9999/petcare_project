from django.shortcuts import render, redirect, get_object_or_404
from .forms import PetForm
from .models import Pet
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def add_pet(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            return redirect('dashboard')
    else:
        form = PetForm()
    return render(request, 'pets/add_pet.html', {'form': form})

@login_required
def my_pets(request):
    pets = Pet.objects.filter(owner=request.user)
    return render(request, 'pets/my_pets.html', {'pets': pets})

@login_required
def edit_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES, instance=pet)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pet updated successfully.')
            return redirect('dashboard')
    else:
        form = PetForm(instance=pet)
    return render(request, 'pets/edit_pet.html', {'form': form})

@login_required
def delete_pet(request, pk):
    pet = get_object_or_404(Pet, pk=pk, owner=request.user)
    if request.method == 'POST':
        pet.delete()
        messages.success(request, 'Pet deleted successfully.')
        return redirect('dashboard')
    return render(request, 'pets/delete_pet.html', {'pet': pet})


from django.shortcuts import render, get_object_or_404
from .models import Pet

def pet_detail(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    return render(request, 'pets/pet_detail.html', {'pet': pet})
