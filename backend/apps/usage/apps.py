from django.apps import AppConfig


class UsageConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.usage"
    verbose_name = "Usage & Quotas"

    def ready(self):
        import apps.usage.signals  # noqa: F401
