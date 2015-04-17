from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from imageconv.models import Image
from imageconv.forms import FileUploadForm

from django.conf import settings

def list(request):
    # Handle file upload
    image = None
    error_msg = None
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image(form.cleaned_data['upload_image'])
            if image.get_size() <= int(settings.MAX_UPLOAD_SIZE):
                image.save()
            else:
                error_msg = "This file is too big! Please upload a file smaller than " + sizeof_fmt(int(settings.MAX_UPLOAD_SIZE))

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('imageconv:list'))
    else:
        form = FileUploadForm() # A empty, unbound form

    # Load images for the list page
    images = None

    # Render list page with the documents and the form
    return render_to_response(
        'imageconv/list.html',
        {'image': image, 'form': form, 'error_msg': error_msg, 'max_size': sizeof_fmt(int(settings.MAX_UPLOAD_SIZE))},
        context_instance=RequestContext(request)
    )

def sizeof_fmt(num, suffix='B'):
    """Takes a size (number of units) and the unit as an input and returns a human readable string"""
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)