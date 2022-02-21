from django.db import models
from django.contrib.auth.models import User
from tinymce.models import HTMLField


class Categorys(models.Model):
    name = models.CharField(max_length=64, unique=True)
    sort = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=256)
    text = models.TextField()
    content = HTMLField()
    cats = models.ForeignKey(Categorys, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Clicks(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    #changed = models.DateTimeField(blank=True)
    show = models.BooleanField(default=False)

