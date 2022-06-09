from django.contrib.auth.models import User
from django.db import models


class Conversion(models.Model):
    files_number = models.IntegerField


class Upload(models.Model):
    title = models.CharField(max_length=30)


class Converter(models.Model):
    files = models.FileField(help_text="Add files that you want to convert.", default=None, null=False)
    upload = models.ForeignKey(Upload, related_name="files",
                               on_delete=models.CASCADE)

