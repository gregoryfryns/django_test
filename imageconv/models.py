from django.db import models
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

# Create your models here.
img_temp = NamedTemporaryFile(delete=True)
img_temp.write(urllib2.urlopen(url).read())
img_temp.flush()

im.file.save(img_filename, File(img_temp))
