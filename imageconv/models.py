import os
import boto3
from boto3.session import Session
from io import BytesIO

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
from django.db import models
from PIL import Image, ImageFilter

from django_rq import job

# Model
class UploadedImage(models.Model):
    def __init__(self, image_file):
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)
        self.local_path = default_storage.save(settings.MEDIA_ROOT + '/', ContentFile(image_file.read()))
        self.name, self.extension = os.path.splitext(image_file.name)
        self.size = image_file.size

        # Save file in Amazon S3 bucket
        try:
            self.s3_path = self.local_path[len(settings.MEDIA_ROOT)+1:] + '/' + image_file.name
            session = Session(aws_access_key_id=settings.AWS_ACCESS_KEY,
                      aws_secret_access_key=settings.AWS_SECRET_KEY,
                      region_name=settings.REGION_NAME)
            s3 = session.resource('s3')
            bitstream = open(self.local_path, 'rb')
            s3.Bucket(settings.S3_BUCKET).put_object(Key=self.s3_path, Body=bitstream)
        except ClientError:
            # Error: impossible to access the bucket
            raise


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

    def get_local_path(self):
        return self.local_path

    def get_s3_path(self):
        return self.s3_path

@job
def apply_filter(pickled_img, option, target_url):
    """Apply Pillow module's filter to the image given as an argument and saves the newly
    created image in the Amazon S3 bucket, under the path given as target_url.
    The arguments are :
        - pickled_img: a dictinary containing the following elements
                'local_path': image path on the local drive
                'name': original image name (without extension)
                'ext': original image extension
        - option: the name of the filter to be applied. Valid filters are BLUR, CONTOUR, 
                DETAIL, EDGE_ENHANCE, EDGE_ENHANCE_MORE, EMBOSS, FIND_EDGES, SMOOTH, 
                SMOOTH_MORE and SHARPEN
        - target_url: the path to be used to store the result, in the S3 bucket defined 
                in the settings
    """

    im = Image.open(pickled_img['local_path'])

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
        raise NotImplementedError('Filter "' + option + '" cannot be applied to the image!')

    # Save result in Amazon S3 bucket
    session = Session(aws_access_key_id=settings.AWS_ACCESS_KEY,
              aws_secret_access_key=settings.AWS_SECRET_KEY,
              region_name=settings.REGION_NAME)
    s3 = session.resource('s3')
    cimage = BytesIO()
    im.save(cimage, format=guess_image_format(pickled_img['ext']))
    s3.Bucket(settings.S3_BUCKET).put_object(Key=target_url, Body=cimage.getvalue())

    return target_url

def guess_image_format(ext):
    ext_dict = {
        ".bmp": "BMP",
        ".dib": "BMP",
        ".dcx": "DCX",   
        ".eps": "EPS",
        ".ps" : "EPS",
        ".gif": "GIF",
        ".im" : "IM",
        ".jpg": "JPEG",
        ".jpe": "JPEG",
        ".jpeg": "JPEG",
        ".pcd": "PCD",
        ".pcx": "PCX",
        ".pdf": "PDF",
        ".png": "PNG",
        ".pbm": "PPM",
        ".pgm": "PPM",
        ".ppm": "PPM",
        ".psd": "PSD",
        ".tif": "TIFF",
        ".tiff": "TIFF",
        ".xbm": "XBM",
        ".xpm": "XPM",
    }
    return ext_dict[ext]