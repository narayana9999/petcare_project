from django.db import models
from accounts.models import User

# Create your models here.

class Guide(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    pet_type = models.CharField(max_length=100)  # e.g., Dog, Cat, Rabbit
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
