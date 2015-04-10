from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from imageconv.models import Image
from imageconv.forms import ImageUploadForm

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image(imgFile = request.FILES['file'])
            image.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('imageconv.views.list'))
    else:
        form = ImageUploadForm() # A empty, unbound form

    # Load images for the list page
    images = Image.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'imageconv/list.html',
        {'images': images, 'form': form},
        context_instance=RequestContext(request)
    )