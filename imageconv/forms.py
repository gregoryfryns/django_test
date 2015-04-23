from django import forms
from django.conf import settings

# Helper function to convert file sizes in a readable format
def sizeof_fmt(num, suffix='B'):
    """Takes a size (number of units) and the unit as an input and returns a human readable string"""
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Y', suffix)

class FileUploadForm(forms.Form):
    upload_image = forms.ImageField(
        label='Select a file',
        help_text='(max. %s)' % sizeof_fmt(int(settings.MAX_UPLOAD_SIZE))
    )
