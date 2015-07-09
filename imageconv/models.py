import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models
from PIL import Image, ImageFilter

from django_rq import job

# Create your models here.
class UploadedImage(models.Model):
    def __init__(self, image_file):
        # TODO: save image with original name
        self.path = default_storage.save('uploaded_images/', ContentFile(image_file.read()))
        self.name, self.extension = os.path.splitext(image_file.name)
        self.size = image_file.size

    def get_size(self):
        return self.size

    def get_mode(self):
        return self.mode

    def get_name(self):
        return self.name

    def get_ext(self):
        return self.extension

    def get_format(self):
        return self.format

    def get_path(self):
        return self.path

@job
def apply_filter(pickled_img, option):
    """Apply Pillow module's filter to the image given as an argument and saves the
    modified at the path returned.
    The arguments are :
        - pickled_img: a dictinary containing the following elements
                'path': original image path
                'name': original image name (without extension)
                'ext': original image extension
        - option: the name of the filter to be applied. Valid filters are BLUR, CONTOUR, 
                DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, 
                SMOOTH_MORE and SHARPEN
    """

    im = Image.open(settings.MEDIA_ROOT + '/' + pickled_img['path'])

    filters_dir = pickled_img['path'] + '_filters'

    if not os.path.exists(settings.MEDIA_ROOT + '/' + filters_dir):
        os.makedirs(settings.MEDIA_ROOT + '/' + filters_dir)

    filter_path = filters_dir + '/' + pickled_img['name'] + '_' + option + pickled_img['ext']
    # filter_path = '%(path)s/%(name)s_%(option)s%(ext)s' % \
    #     {"path": filters_dir, "name": pickled_img['name'], "option": option, "ext": pickled_img['ext']}

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
            return settings.MEDIA_URL + pickled_img['path']

    # Save file with absolute URL
    im.save(settings.MEDIA_ROOT + '/' + filter_path)
    # Return relative URL
    return settings.MEDIA_URL + filter_path
