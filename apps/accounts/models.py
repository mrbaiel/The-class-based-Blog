from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from django.views.defaults import server_error

from apps.services.utils import unique_slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(verbose_name='URL', max_length=100, blank=True, unique=True)
    avatar = models.ImageField(
        verbose_name='Аватарка',
        upload_to='images/avatars/%Y/%m/%d/',
        default='images/avatars/default.jpeg',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpeg', 'png', 'jpg'])]
    )
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')
    birth_data = models.DateTimeField(null=True, blank=True, verbose_name='Дата рождения')

    class Meta:
        '''
        Sorting the name of the table in the db
        '''
        ordering = ('user',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def save(self, *args, **kwargs):
        """
                 Сохранение полей модели при их отсутствии заполнения

        """
        if not self.slug:
            self.slug = unique_slugify(self, self.user.username, self.slug)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username

    def get_ablosute_url(self):
        return reverse('profile_detail', kwargs={'slug': self.slug})


    def is_online(self):
        cache_key = f"last-seen-{self.user.id}"
        last_seen = cache.get(cache_key)

        if last_seen is not None:
            return True
        return False