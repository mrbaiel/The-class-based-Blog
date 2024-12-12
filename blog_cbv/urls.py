from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings

handler403 = 'apps.blog.views.tr_handler403'
handler404 = 'apps.blog.views.tr_handler404'
handler500 = 'apps.blog.views.tr_handler500'

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include('apps.blog.urls')),
    path('', include('apps.accounts.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]