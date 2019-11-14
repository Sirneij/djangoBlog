from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from PIL import Image
from markdown_deux import markdown


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    about = models.TextField()

    def __str__(self):
        return f'{self.user.username} Profile'

    def get_markdown(self):
        about = self.about
        markdown_text = markdown(about)
        return mark_safe(markdown_text)

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 150 or img.width > 150:
            output_size = (150, 150)
            img.thumbnail(output_size)
            img.save(self.image.path)
