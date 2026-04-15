"""
Accounts app — Admin configuration.

Registers InviteCode in Django admin so you can generate and manage
invite codes from the admin panel on your phone.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import InviteCode, User


@admin.register(User)
class CompanionUserAdmin(UserAdmin):
    list_display = ("username", "language_preference", "voice_preference", "is_age_verified", "created_at")


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "max_uses", "times_used", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("code", "label")
    readonly_fields = ("times_used", "created_at")
