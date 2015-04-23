from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from imageconv.models import Image
from imageconv.forms import FileUploadForm

from django.conf import settings

def list(request):
    # Get information of the last image uploaded by the user from the session
    error_msg = None
    image_name = None
    image_size = None
    image_path = None

    if 'error_msg' in request.session:
        error_msg = request.session['error_msg']
        del request.session['error_msg']

    if 'image_name' in request.session:
        image_name = request.session['image_name']

    if 'image_size' in request.session:
        image_size = request.session['image_size']

    if 'image_path' in request.session:
        image_path = request.session['image_path']

    # Handle the file uploaded via the form
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # TODO: validate data
            image = Image(form.cleaned_data['upload_image'])
            if image.get_size() <= int(settings.MAX_UPLOAD_SIZE):
                image.save()
                request.session['image_name'] = image.get_name()
                request.session['image_size'] = sizeof_fmt(image.get_size())
                request.session['image_path'] = image.get_path()
            else:
                request.session['error_msg'] = "This file is too big! Please upload a file smaller than " + sizeof_fmt(int(settings.MAX_UPLOAD_SIZE))

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('imageconv:list'))
    else:
        form = FileUploadForm() # A empty, unbound form


    # Render list page with the image info
    context = {'image_name': image_name,
               'image_size': image_size,
               'image_url': settings.MEDIA_URL + image_path,
               'form': form,
               'error_msg': error_msg,
               'max_upload_size': sizeof_fmt(int(settings.MAX_UPLOAD_SIZE))

    }
    return render_to_response(
        'imageconv/list.html',
        context,
        context_instance=RequestContext(request)
    )

# Helper function to convert file sizes in a readable format
def sizeof_fmt(num, suffix='B'):
    """Takes a size (number of units) and the unit as an input and returns a human readable string"""
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)
