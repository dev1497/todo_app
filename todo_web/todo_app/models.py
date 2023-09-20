from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ("Completed", "Completed" ),
        ("Not Completed", "Not Completed" )
    ]
    title = models.TextField(max_length=50)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='Not Completed')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return(f"{self.title}")

    def clean(self):
        if self.expire_at and self.expire_at < timezone.now():
            raise ValidationError("The expiration date must be in the future.")