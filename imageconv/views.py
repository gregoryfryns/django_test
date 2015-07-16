import os
import django_rq
from django.conf import settings

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.template.defaultfilters import filesizeformat

from imageconv.models import UploadedImage, apply_filter
from imageconv.forms import ImageUploadForm

def imageconv(request):
    # List of filters to be applied
    applied_filters = ['BLUR', 
                        'CONTOUR',
                        'EMBOSS']

    # Get information of last uploaded image from the session
    image_name = None
    image_extension = None
    image_size = None
    image_s3_dir = None

    if 'image_name' in request.session:
        image_name = request.session['image_name']

    if 'image_extension' in request.session:
        image_extension = request.session['image_extension']

    if 'image_size' in request.session:
        image_size = request.session['image_size']

    if 'image_s3_dir' in request.session:
        image_s3_dir = request.session['image_s3_dir']

    # Handle the file uploaded via the form
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = UploadedImage(form.cleaned_data['upload_image'])
            
            # Store new info in session
            request.session['image_name'] = image.get_name()
            request.session['image_size'] = filesizeformat(image.get_size())
            request.session['image_s3_dir'] = settings.AWS_S3_BASE_URL + os.path.split(image.get_s3_path())[0]
            request.session['image_extension'] = image.get_ext()

            # Prepare image for handling by worker process
            pickled_img = {
                'local_path': image.get_local_path(),
                'name': image.get_name(),
                'ext': image.get_ext(),
            }

            for filter_name in applied_filters :
                # Build s3 url to be used
                filename, ext = os.path.splitext(image.get_s3_path())
                filter_s3_path = filename + "_" + filter_name + ext

                # Send job to worker process
                apply_filter.delay(pickled_img, filter_name, filter_s3_path)

            # Redirect to the document imageconv after POST
            return HttpResponseRedirect(reverse('imageconv:upload'))
    else:
        form = ImageUploadForm() # A empty, unbound form

    # Render page with the image info
    context = {'image_name': image_name,
               'image_size': image_size,
               'image_s3_dir': image_s3_dir,
               'image_extension': image_extension,
               'applied_filters': applied_filters,
               'form': form,
               'max_upload_size': filesizeformat(settings.MAX_UPLOAD_SIZE),
    }

    return render_to_response(
        'imageconv/index.html',
        context,
        context_instance=RequestContext(request)
    )
