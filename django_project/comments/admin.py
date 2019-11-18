from django.contrib import admin
from django.db import models
# Register your models here.
from .models import Comment
from pagedown.widgets import AdminPagedownWidget


class PostAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.TextField: {'widget': AdminPagedownWidget },
}

admin.site.register(Comment, PostAdmin)