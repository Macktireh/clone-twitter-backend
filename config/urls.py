from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views.static import serve

from rest_framework import routers

from config.settings.base import ENV
from apps.profiles.urls import router as router_profile


router = routers.DefaultRouter()
router.registry.extend(router_profile.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('apps.account.urls')),
    # path('api/profile/', include('apps.profiles.urls')),
    path('api/profile/', include(router.urls)),
]

if ENV == 'development':
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    else:
        urlpatterns += [re_path(r'^mediafiles/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),]
else:
    urlpatterns += [re_path(r'^mediafiles/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),]