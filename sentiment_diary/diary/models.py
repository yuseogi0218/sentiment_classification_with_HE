from django.db import models
from django.contrib.auth.models import User


class Diary(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    sentiment = models.TextField()
    create_date = models.DateTimeField()
