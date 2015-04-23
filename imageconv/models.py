import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models

# Create your models here.
class Image(models.Model):
    def __init__(self, image_file):
        self.img_file = image_file
        self.name = image_file.name
        self.size = image_file.size
        self.path = None

    def get_size(self):
        return self.size

    def get_name(self):
        return self.name

    def get_format(self):
        return self.format

    def get_path(self):
        return self.path

    def save(self):
        # TODO: remove older files if too much space is used
        self.path = default_storage.save('uploaded_images/', ContentFile(self.img_file.read()))
