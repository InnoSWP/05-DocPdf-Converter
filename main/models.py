from django.contrib.auth.models import User
from django.db import models


class Conversion(models.Model):
    files_number = models.IntegerField

class Upload(models.Model):
    title = models.CharField(max_length=30)


class Converter(models.Model):
    token = models.TextField(max_length=36, help_text="Enter your token.", default=None)
    files = models.FileField(help_text="Add files that you want to convert.", default=None)
    upload = models.ForeignKey(Upload, related_name="files",
                               on_delete=models.CASCADE)

