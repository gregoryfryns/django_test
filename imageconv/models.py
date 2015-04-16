import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models

# Create your models here.
class Image(models.Model):
    img_file = models.ImageField(upload_to='uploaded_images/%Y/%m/%d')
