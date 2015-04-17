import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models

# Create your models here.
class Image(models.Model):
    def __init__(self, image_file):
        self.img_file = image_file

    def get_size(self):
        return self.img_file.size

    def save(self):
        path = default_storage.save('uploaded_images/', ContentFile(self.img_file.read())) 
#    img_file = models.ImageField(upload_to='uploaded_images/%Y/%m/%d')
