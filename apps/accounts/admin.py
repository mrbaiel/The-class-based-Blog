from django.contrib import admin

from apps.accounts.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'birth_data', 'slug')
    list_display_links = ('user', 'slug')
    prepopulated_fields ={'slug': ('user',)}