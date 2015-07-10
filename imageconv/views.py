from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.template.defaultfilters import filesizeformat

from imageconv.models import UploadedImage, apply_filter
from imageconv.forms import ImageUploadForm

from django.conf import settings
import django_rq

def imageconv(request):
    # List of filters to be applied
    applied_filters = ['BLUR', 
                        'CONTOUR', 
                        'DETAIL']

    # Get information of the last image uploaded by the user from the session
    image_name = None
    image_ext = None
    image_size = None
    image_tempfile = None

    if 'image_name' in request.session:
        image_name = request.session['image_name']

    if 'image_ext' in request.session:
        image_ext = request.session['image_ext']

    if 'image_size' in request.session:
        image_size = request.session['image_size']

    if 'image_tempfile' in request.session:
        image_tempfile = settings.MEDIA_URL + request.session['image_tempfile']

    # Handle the file uploaded via the form
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = UploadedImage(form.cleaned_data['upload_image'])
            
            request.session['image_name'] = image.get_name()
            request.session['image_size'] = filesizeformat(image.get_size())
            request.session['image_tempfile'] = image.get_temp_file_name()
            request.session['image_ext'] = image.get_ext()

            pickled_img = {
                'absolute_path': image.get_absolute_path(),
                'name': image.get_name(),
                'ext': image.get_ext(),
            }

            for filter_name in applied_filters :
                # apply filter using background process
                apply_filter.delay(pickled_img, filter_name)

            # Redirect to the document imageconv after POST
            return HttpResponseRedirect(reverse('imageconv:upload'))
    else:
        form = ImageUploadForm() # A empty, unbound form

    # Render page with the image info
    context = {'image_name': image_name,
               'image_size': image_size,
               'image_tempfile': image_tempfile,
               'image_ext': image_ext,
               'applied_filters': applied_filters,
               'form': form,
               'max_upload_size': filesizeformat(settings.MAX_UPLOAD_SIZE),
    }

    return render_to_response(
        'imageconv/index.html',
        context,
        context_instance=RequestContext(request)
    )
