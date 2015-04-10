from django import forms

class ImageUploadForm(forms.Form):
    file = forms.FileField(
        label='Select a picture',
        help_text='max. 2 megabytes'
    )