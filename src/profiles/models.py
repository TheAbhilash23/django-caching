from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.
UserModel = get_user_model()


class Profile(models.Model):
    ProfileId = models.BigAutoField(
        _('Id'),
        primary_key=True
    )
    User = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name='UserProfile'
    )
    Picture = models.ImageField(
        _('Picture'),
        upload_to='uploads/profile_images',
    )

    def __str__(self):
        return f'{self.User}'

    class Meta:
        db_table = 'Profile'
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
