import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class InviteCode(models.Model):
    """
    Access control for Companion OS registration.

    Why invite codes?
    This app serves vulnerable people. Open registration means anyone can
    sign up, including bad actors. Invite codes let Liina control who gets
    access during early testing and beyond.

    Each code can be single-use or multi-use (max_uses).
    Once used up, it cannot be reused.
    """

    code = models.CharField(
        max_length=40,
        unique=True,
        default=uuid.uuid4,
        help_text="The invite code users enter during registration.",
    )
    label = models.CharField(
        max_length=100,
        blank=True,
        help_text="Who is this code for? e.g. 'Niina testing', 'Jon demo'",
    )
    max_uses = models.PositiveIntegerField(
        default=1,
        help_text="How many times this code can be used. 0 = unlimited.",
    )
    times_used = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        status = "active" if self.is_active and not self.is_exhausted else "used up"
        return f"{self.label or self.code} ({status})"

    @property
    def is_exhausted(self):
        """True if the code has been used up (max_uses > 0 and reached)."""
        if self.max_uses == 0:
            return False  # unlimited
        return self.times_used >= self.max_uses

    @property
    def is_valid(self):
        """True if this code can still be used."""
        return self.is_active and not self.is_exhausted

    def use(self):
        """Mark one use of this code."""
        self.times_used += 1
        self.save(update_fields=["times_used"])


class User(AbstractUser):
    """
    Custom User model for Companion OS.

    Why extend AbstractUser instead of using Django's default?
    Because we need fields Django doesn't have by default:
    - language preference (Finnish, Estonian, English)
    - voice preference (Warm, Sharp, Steady, Spark, Coach)
    - age verification status (for under-18 parental consent flow)

    If we used Django's default User and later needed these fields,
    we'd have to do a complex migration. Setting this on day one costs nothing.
    """

    LANGUAGE_CHOICES = [
        ("fi", "Finnish"),
        ("et", "Estonian"),
        ("en", "English"),
    ]

    VOICE_CHOICES = [
        ("steady", "Steady"),  # default — calm, no drama
        ("warm", "Warm"),
        ("sharp", "Sharp"),
        ("spark", "Spark"),
        ("coach", "Coach"),
    ]

    language_preference = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default="en",
    )
    voice_preference = models.CharField(
        max_length=10,
        choices=VOICE_CHOICES,
        default="steady",
    )
    is_age_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username
