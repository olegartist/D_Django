from django.db import models
from django.contrib.auth.models import User

class Accounts(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=10)
    code_time = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    time_zone = models.CharField(max_length=20)

