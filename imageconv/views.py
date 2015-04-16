from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from imageconv.models import Image
from imageconv.forms import FileUploadForm

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['upload_image']
            path = default_storage.save('uploaded_images/%Y/%m/%d', ContentFile(image.read())) 
            tmp_file = os.path.join(settings.MEDIA_ROOT, path)
#            image = Image(request.FILES['upload_image'])
#            image.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('imageconv:list'))
    else:
        form = FileUploadForm() # A empty, unbound form

    # Load images for the list page
#    images = Image.objects.all()
    images = None

    # Render list page with the documents and the form
    return render_to_response(
        'imageconv/list.html',
        {'images': images, 'form': form, 'coucou': "no coucou"},
        context_instance=RequestContext(request)
    )