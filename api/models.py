from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    pass

class Group(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    budget=models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    admin=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
