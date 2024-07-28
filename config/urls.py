from docs.swagger import schema_view
from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf.urls.static import static

from apps.home.views import home


urlpatterns = [
    path("", home, name="home"),
    path("admin/docs", include("django.contrib.admindocs.urls")),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/auth/user/", include("apps.authentication.urls")),
    path("api/users/", include("apps.profiles.urls")),
    path("api/posts/", include("apps.post.urls")),
    path("api/comments/", include("apps.comment.urls")),
    path("api/follow/", include("apps.follow.urls")),
    path("api/notifications/", include("apps.notification.urls")),
    path("api/bookmarks/", include("apps.bookmark.urls")),
    path("api/chat/", include("apps.chat.urls")),
    re_path(
        r"^docs(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    re_path(
        r"^api/docs/$", schema_view.with_ui("swagger", cache_timeout=0), name="docs-api"
    ),
    # re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.ENV == 'development':
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     if settings.DEBUG:
#     else:
#         urlpatterns += [re_path(r'^mediafiles/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),]
# else:
#     urlpatterns += [re_path(r'^mediafiles/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),]
