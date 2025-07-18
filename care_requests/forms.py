from django import forms
from .models import CareRequest, Application
from pets.models import Pet

class CareRequestForm(forms.ModelForm):
    class Meta:
        model = CareRequest
        fields = ['pet', 'start_date', 'end_date', 'location', 'instructions']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if self.user:
            self.fields['pet'].queryset = Pet.objects.filter(owner=self.user)

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['message']
