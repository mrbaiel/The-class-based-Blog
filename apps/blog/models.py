from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel

from apps.services.utils import unique_slugify


class PostManager(models.Manager):
    """
    Кастомный менеджер постов
    """
    def get_queryset(self):
        return super().get_queryset().select_related("author","category").filter(status='published')

class Post(models.Model):
    """
    Модель постов для нашего блога
    """

    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )

    title = models.CharField(max_length=90, verbose_name="Название записи")
    slug = models.SlugField(max_length=90, verbose_name="URL", blank=True)
    description = models.TextField(max_length=300, verbose_name="Описание")
    text = models.TextField(verbose_name="Запись")
    thumbnail = models.ImageField(
        default='default.jpg',
        verbose_name="Изображение записи",
        blank=True,
        upload_to='images/thumbnails/',
        validators=[FileExtensionValidator(
            allowed_extensions=('png', 'jpg', 'webp', 'jpeg', 'gif')
        )]
    )
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус записи', max_length=10)
    create = models.DateTimeField(auto_now_add=True, verbose_name='Время добавления')
    update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    author = models.ForeignKey(to=User, verbose_name='Автор', on_delete=models.SET_DEFAULT, related_name='author_posts',
                               default=1)
    updater = models.ForeignKey(to=User, verbose_name='Кто обновил', on_delete=models.SET_NULL, null=True,
                                related_name='updater_posts', blank=True)
    fixed = models.BooleanField(verbose_name='Прикреплено', default=False)
    category = TreeForeignKey('Category', on_delete=models.PROTECT, related_name='posts', verbose_name='Категория')
    objects = models.Manager()
    custom = PostManager()

    class Meta:
        db_table = 'blog_post'
        ordering = ['-fixed', '-create']
        indexes = [models.Index(fields=['-fixed', '-create', 'status'])]
        verbose_name = 'Запись'
        verbose_name_plural = 'Записи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Получаем ссылку на статью
        """
        return reverse('post_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = unique_slugify(self, self.title, self.slug)
        super().save(*args, **kwargs)


class Category(MPTTModel):
    """
    Модель категорий с вложенностью
    """

    title = models.CharField(max_length=50, verbose_name='Название категории')
    slug = models.SlugField(max_length=100, verbose_name='URL категории', blank=True)
    description = models.TextField(verbose_name='описание категории', max_length=255)
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        db_index=True,
        related_name='children',
        verbose_name='Родительская категория',
    )

    class MPTTMeta:
        """
        Сортировка по вложенности
        """
        order_insertion_by = ('title',)

    class Meta:
        """
        Сортировка, название модели в админке
        """
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"
        db_table = 'app_categories'

    def get_absolute_url(self):
        return reverse('post_by_category', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(MPTTModel):
    """
    не простые а древовидные комментарии)
    """
    STATUS_OPTIONS = (
        ('published', 'Опубликовано'),
        ('draft', 'Черновик')
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='запись', related_name='comments')
    author = models.ForeignKey(User, verbose_name='Автор комментария', on_delete=models.CASCADE,
                               related_name='comments_author')
    content = models.TextField(verbose_name='Текст комментария', max_length=3000)
    time_create = models.DateTimeField(verbose_name='Время добавления', auto_now_add=True)
    time_update = models.DateTimeField(verbose_name='Время обновления', auto_now=True)
    status = models.CharField(choices=STATUS_OPTIONS, default='published', verbose_name='Статус поста', max_length=10)
    parent = TreeForeignKey('self', verbose_name='Родительский комментарий', null=True, blank=True,
                            related_name='children', on_delete=models.CASCADE)

    class MTTMeta:
        """
        Сортировуем по вложенносит
        """
        order_insertion_by = ('-time_create',)

    class Meta:
        """
        Сортировка, название модели в админ панели, таблица в данными
        """
        ordering = ['-time_create']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return f'{self.author}:{self.content}'