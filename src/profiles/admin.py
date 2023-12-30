from django.contrib import admin
from profiles import models
# Register your models here.


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'User', 'Picture',
    )
