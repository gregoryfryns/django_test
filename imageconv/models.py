from django.db import models

# Create your models here.
class Image(models.Model):
    img_file = models.FileField(upload_to='uploadedImages/%Y/%m/%d')
