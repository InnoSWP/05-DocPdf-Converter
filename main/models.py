from django.contrib.auth.models import User
from django.db import models


class Upload(models.Model):
    title = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Converter(models.Model):
    files = models.FileField()
    upload = models.ForeignKey(Upload, related_name="files", on_delete=models.CASCADE)
