from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username', 'email', 'password1', 'password2',
            'is_owner', 'is_sitter', 'bio', 'location', 'phone_number', 'profile_picture'
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        # Save custom fields
        user.email = self.cleaned_data['email']
        user.is_owner = self.cleaned_data['is_owner']
        user.is_sitter = self.cleaned_data['is_sitter']
        user.bio = self.cleaned_data['bio']
        user.location = self.cleaned_data['location']
        user.phone_number = self.cleaned_data['phone_number']
        user.profile_picture = self.cleaned_data.get('profile_picture')

        if commit:
            user.save()

        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'bio', 'location', 'phone_number', 'profile_picture']


from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
