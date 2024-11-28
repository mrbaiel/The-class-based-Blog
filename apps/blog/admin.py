from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

from .models import Post, Category


@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ панель модели категорий
    """
    prepopulated_fields = {'slug':('title',)}

admin.site.register(Post)