from django.db import models
from accounts.models import User
from pets.models import Pet

# Create your models here.

class CareRequest(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    is_fulfilled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet.name} ({self.start_date} to {self.end_date})"

class Application(models.Model):
    care_request = models.ForeignKey(CareRequest, on_delete=models.CASCADE)
    sitter = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sitter.username} → {self.care_request}"
