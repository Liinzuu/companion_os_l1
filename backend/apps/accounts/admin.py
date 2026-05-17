"""
Accounts app — Admin configuration.

Registers InviteCode in Django admin so you can generate and manage
invite codes from the admin panel on your phone.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import InviteCode, ImpactSurvey, PartnershipInquiry, PilotApplication, User


@admin.register(User)
class CompanionUserAdmin(UserAdmin):
    list_display = ("username", "language_preference", "is_age_verified", "created_at")


@admin.register(InviteCode)
class InviteCodeAdmin(admin.ModelAdmin):
    list_display = ("code", "label", "max_uses", "times_used", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("code", "label")
    readonly_fields = ("times_used", "created_at")


@admin.register(ImpactSurvey)
class ImpactSurveyAdmin(admin.ModelAdmin):
    list_display = ("user", "survey_type", "handle_difficult_moments", "notice_stress_building", "have_something_to_try", "get_through_daily_tasks", "age_range", "situation_display", "country", "created_at")
    list_filter = ("survey_type",)
    readonly_fields = ("created_at",)

    _SITUATION_LABELS = {
        "working_ft": "Working full time",
        "working_pt": "Working part time",
        "studying_ft": "Studying full time",
        "studying_pt": "Studying part time",
        "parent": "Parent or caregiver",
    }

    @admin.display(description="Situation")
    def situation_display(self, obj):
        if not obj.situation:
            return "—"
        return ", ".join(self._SITUATION_LABELS.get(s, s) for s in obj.situation)


@admin.register(PilotApplication)
class PilotApplicationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("name", "email")
    readonly_fields = ("created_at",)


@admin.register(PartnershipInquiry)
class PartnershipInquiryAdmin(admin.ModelAdmin):
    list_display = ("organization_name", "contact_person", "email", "organization_type", "country", "status", "created_at")
    list_filter = ("status", "organization_type", "country")
    search_fields = ("organization_name", "contact_person", "email")
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Organization", {
            "fields": ("organization_name", "organization_type", "country", "target_population"),
        }),
        ("Contact", {
            "fields": ("contact_person", "role", "email", "phone"),
        }),
        ("Inquiry", {
            "fields": ("what_brings_you", "status", "notes"),
        }),
        ("Metadata", {
            "fields": ("created_at",),
        }),
    )
