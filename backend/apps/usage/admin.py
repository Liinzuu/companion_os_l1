from django.contrib import admin

from .models import UsageEvent, UsageQuota


@admin.register(UsageQuota)
class UsageQuotaAdmin(admin.ModelAdmin):
    """
    Admin for per-user quotas.
    Liina can bump individual user limits from here
    if someone genuinely needs more conversations.
    """

    list_display = [
        "user",
        "daily_used",
        "daily_limit",
        "monthly_used",
        "monthly_limit",
        "last_daily_reset",
    ]
    list_editable = ["daily_limit", "monthly_limit"]
    search_fields = ["user__username"]
    list_filter = ["daily_limit", "monthly_limit"]


@admin.register(UsageEvent)
class UsageEventAdmin(admin.ModelAdmin):
    """
    Read-only log of usage events.
    Only contains events for users who consented to tracking.
    """

    list_display = ["user", "event_type", "created_at"]
    list_filter = ["event_type", "created_at"]
    search_fields = ["user__username"]
    readonly_fields = ["user", "event_type", "created_at"]
