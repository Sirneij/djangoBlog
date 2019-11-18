from django.contrib import admin
from .models import Profile

from django.db import models

from pagedown.widgets import AdminPagedownWidget
class UserAdmin(admin.ModelAdmin):
        formfield_overrides = {
            models.TextField: {'widget': AdminPagedownWidget },
        }

admin.site.register(Profile, UserAdmin)
