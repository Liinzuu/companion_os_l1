"""
Auto-create UsageQuota when a new user registers.

Why a signal instead of putting this in the registration view?
Because users can also be created from the Django admin, from
management commands, or from the auto-superuser creation on deploy.
A signal catches all of those paths. The registration view is just one.
"""
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UsageQuota


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_usage_quota(sender, instance, created, **kwargs):
    if created:
        UsageQuota.objects.get_or_create(user=instance)
