from django.db import models
from accounts.models import User

# Create your models here.

class Pet(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)  # e.g., Dog, Cat
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='pets/', blank=True, null=True)

    def __str__(self):
        return self.name
