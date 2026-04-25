"""
Safety app — Admin configuration.

Registers SystemConfig (the kill switch) and SafetyEvent (audit log)
in Django admin. The kill switch is the single most important admin
page — it must be reachable from any device, in under 60 seconds.
"""
from django.contrib import admin

from .models import SafetyEvent, SystemConfig


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    """
    The kill switch admin.

    Single row (pk=1, enforced by the model's save() method).
    Toggling maintenance_mode pauses the entire app for users.
    /admin/ remains accessible so the operator can flip it back off.
    """

    list_display = ("__str__", "maintenance_mode", "updated_at")
    fields = ("maintenance_mode", "maintenance_message")

    def has_add_permission(self, request):
        # Singleton — only one row should ever exist.
        return not SystemConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Never deletable — losing this row would lose the kill switch.
        return False


@admin.register(SafetyEvent)
class SafetyEventAdmin(admin.ModelAdmin):
    """
    Read-only audit log of safety tier triggers.

    No conversation content stored here — only the tier, timestamp,
    and a SHA-256 hashed signal. Safe to view, safe under subpoena.
    """

    list_display = ("triggered_at", "tier", "user")
    list_filter = ("tier", "triggered_at")
    readonly_fields = ("user", "tier", "signal_hash", "triggered_at")

    def has_add_permission(self, request):
        return False
