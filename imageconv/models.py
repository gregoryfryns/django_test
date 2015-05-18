import os
import re
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models
from PIL import Image, ImageFilter

# Create your models here.
class UploadedImage(models.Model):
    def __init__(self, image_file):
        self.img_file = image_file
        self.name, self.extension = os.path.splitext(image_file.name)
        self.size = image_file.size
        self.path = None

    def get_size(self):
        return self.size

    def get_name(self):
        return self.name

    def get_ext(self):
        return self.extension

    def get_format(self):
        return self.format

    def get_path(self):
        return self.path

    def save(self):
        # TODO: remove older files if too much space is used
        self.path = default_storage.save('uploaded_images/', ContentFile(self.img_file.read()))

    def filter(self, option):
        """Apply Pillow module's filter and return URL of the modified image. Valid filters are 
        BLUR, CONTOUR, DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, 
        SMOOTH_MORE and SHARPEN"""
        im = Image.open(settings.MEDIA_ROOT + '/' + self.path)

        filter_path = '%(path)s_%(option)s%(ext)s' % \
            {"path": self.path, "name": self.name, "option": option, "ext": self.extension}

        # TODO: start a worker dyno to apply filters
        if not os.path.isfile(settings.MEDIA_ROOT + '/' + filter_path):
            if option == 'BLUR':
                im = im.filter(ImageFilter.BLUR)
            elif option == 'CONTOUR':
                im = im.filter(ImageFilter.CONTOUR)
            elif option == 'DETAIL':
                im = im.filter(ImageFilter.DETAIL)
            elif option == 'EDGE_ENHANCE':
                im = im.filter(ImageFilter.EDGE_ENHANCE)
            elif option == 'EDGE_ENHANCE_MORE':
                im = im.filter(ImageFilter.EDGE_ENHANCE_MORE)
            elif option == 'EMBOSS':
                im = im.filter(ImageFilter.EMBOSS)
            elif option == 'FIND_EDGES':
                im = im.filter(ImageFilter.FIND_EDGES)
            elif option == 'SMOOTH':
                im = im.filter(ImageFilter.SMOOTH)
            elif option == 'SMOOTH_MORE':
                im = im.filter(ImageFilter.SMOOTH_MORE)
            elif option == 'SHARPEN':
                im = im.filter(ImageFilter.SHARPEN)
            else:
                return settings.MEDIA_URL + self.path

        # Save file with absolute URL
        im.save(settings.MEDIA_ROOT + '/' + filter_path)
        # Return relative URL
        return settings.MEDIA_URL + filter_path