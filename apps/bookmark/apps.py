from django.apps import AppConfig


class BookmarkConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.bookmark'
    
    def ready(self):
        import apps.bookmark.signals
