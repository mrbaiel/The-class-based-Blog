from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin, MPTTModelAdmin

from .models import Post, Category, Comment

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    """
    Админ панель модели категорий
    """
    prepopulated_fields = {'slug':('title',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title',)}

@admin.register(Comment)
class CommentAdminPage(MPTTModelAdmin):
    pass

