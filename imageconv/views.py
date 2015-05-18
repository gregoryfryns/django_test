from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.template.defaultfilters import filesizeformat

from imageconv.models import UploadedImage
from imageconv.forms import ImageUploadForm

from django.conf import settings

def imageconv(request):
    # Get information of the last image uploaded by the user from the session
    error_msg = None
    image_name = None
    image_ext = None
    image_size = None
    image_url = None
    filter_path = None

    if 'image_name' in request.session:
        image_name = request.session['image_name']

    if 'image_ext' in request.session:
        image_name = request.session['image_ext']

    if 'image_size' in request.session:
        image_size = request.session['image_size']

    if 'image_path' in request.session:
        image_url = settings.MEDIA_URL + request.session['image_path']

    if 'filter_path' in request.session:
        filter_path = request.session['filter_path']

    # Handle the file uploaded via the form
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = UploadedImage(form.cleaned_data['upload_image'])
            image.save()
            
            request.session['image_name'] = image.get_name() + image.get_ext()
            request.session['image_size'] = filesizeformat(image.get_size())
            request.session['image_path'] = image.get_path()
            request.session['filter_path'] = image.filter("FIND_EDGES")

            # Redirect to the document imageconv after POST
            return HttpResponseRedirect(reverse('imageconv:upload'))
    else:
        form = ImageUploadForm() # A empty, unbound form


    # Render page with the image info
    context = {'image_name': image_name,
               'image_size': image_size,
               'image_url': image_url,
               'filter_path': filter_path,
               'form': form,
               'max_upload_size': filesizeformat(settings.MAX_UPLOAD_SIZE)
    }

    return render_to_response(
        'imageconv/index.html',
        context,
        context_instance=RequestContext(request)
    )
