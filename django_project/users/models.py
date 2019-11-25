from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image
from ckeditor.fields import RichTextField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    about = RichTextUploadingField()

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_markdown(self):
        about = self.about
        return mark_safe(about)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.image.path)
