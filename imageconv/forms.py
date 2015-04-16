from django import forms

class FileUploadForm(forms.Form):
    upload_image = forms.ImageField(
        label='Select a file',
        help_text='max. 2 megabytes'
    )