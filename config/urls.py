from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.views.static import serve

from rest_framework import routers

from docs.swagger import schema_view

from config.settings.base import ENV
from apps.profiles.urls import router as router_profile


router = routers.DefaultRouter()
router.registry.extend(router_profile.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/account/', include('apps.account.urls')),
    path('api/me/', include(router.urls)),
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/api/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if ENV == 'development':
    if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    else:
        urlpatterns += [re_path(r'^mediafiles/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),]
else:
    urlpatterns += [re_path(r'^mediafiles/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),]