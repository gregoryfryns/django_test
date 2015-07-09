from django import forms
from django.template.defaultfilters import filesizeformat
from django.conf import settings

class RestrictedImageField(forms.ImageField):
    def __init__(self, *args, **kwargs):
        self.max_upload_size = kwargs.pop('max_upload_size', None)
        if not self.max_upload_size:
            self.max_upload_size = settings.MAX_UPLOAD_SIZE
        super(RestrictedImageField, self).__init__(*args, **kwargs)
 
    def clean(self, *args, **kwargs):
        data = super(RestrictedImageField, self).clean(*args, **kwargs)
        try:
            if data.size > int(self.max_upload_size):
                raise forms.ValidationError(
                    ('File size must be under %(max_size)s. The uploaded file is %(current_size)s.'),
                    code='invalid size',
                    params={'max_size':filesizeformat(self.max_upload_size), 
                            'current_size':filesizeformat(data.size)},
                )
        except AttributeError:
            pass
 
        return data

class ImageUploadForm(forms.Form):
    upload_image = RestrictedImageField(
        label='Select an image file',
        help_text='(max. %s)' % filesizeformat(settings.MAX_UPLOAD_SIZE)
    )
