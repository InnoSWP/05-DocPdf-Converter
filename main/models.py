from django.contrib.auth.models import User
from django.db import models


class Conversion(models.Model):
    """
    Conversion model

    :param files_number: number of files in conversion
    """
    files_number = models.IntegerField


class Upload(models.Model):
    """
    Upload model

    :param title: title of upload file
    """
    title = models.CharField(max_length=30)


class Converter(models.Model):
    """
    Converter model

    :param files: all files for conversion
    :param upload: instance of :class:`Upload` model
    """
    files = models.FileField(help_text="Add files that you want to convert.", default=None, null=False)
    upload = models.ForeignKey(Upload, related_name="files",
                               on_delete=models.CASCADE)

