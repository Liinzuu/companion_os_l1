from django.conf import settings
from django.db import models

from .fields import EncryptedTextField


class Conversation(models.Model):
    """
    A conversation belongs to one user.
    One user can have many conversations.

    Why separate Conversation from Message?
    Because a conversation is a session — it has a start time, a context,
    a mode history. A message is a single exchange within that session.
    Keeping them separate means we can load just the conversation metadata
    without pulling all the messages, which matters for performance later.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,  # delete conversations if user is deleted
        related_name="conversations",
    )
    title = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="User-editable name for this conversation.",
    )
    started_at = models.DateTimeField(auto_now_add=True)
    active_mode = models.CharField(max_length=50, default="auto")

    class Meta:
        ordering = ["-started_at"]

    def __str__(self):
        return f"{self.user.username} — {self.started_at:%Y-%m-%d %H:%M}"

    @classmethod
    def create_for_user(cls, user):
        """
        The ONE place where conversations are created.

        Why a classmethod instead of just Conversation.objects.create()?
        Jon's recommendation. There are two paths that create conversations:
        1. NewConversationView (user clicks "New chat")
        2. ConversationListView (auto-creates on first visit)
        Both must check the quota. Centralising here prevents drift.

        Returns (conversation, error_message).
        conversation is None if quota is exceeded.
        error_message is empty string if creation succeeded.
        """
        from apps.usage.models import UsageQuota

        quota, _ = UsageQuota.objects.get_or_create(user=user)
        allowed, reason = quota.can_create_conversation()

        if not allowed:
            return None, reason

        conversation = cls.objects.create(user=user)
        quota.increment()

        # Log usage event if user consented to tracking
        if user.consent_usage_tracking:
            from apps.usage.models import UsageEvent
            UsageEvent.objects.create(
                user=user,
                event_type="conversation_created",
            )

        return conversation, ""


class Message(models.Model):
    """
    A single message in a conversation.

    role: 'user' or 'assistant' — mirrors the Claude API format.
    content: encrypted. We store no plaintext conversation content.
    active_mode: which mode was active when this message was sent.
                 Stored per message so we can audit mode transitions.
    """

    ROLE_CHOICES = [
        ("user", "User"),
        ("assistant", "Assistant"),
    ]

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = EncryptedTextField()  # encrypted at rest using Fernet
    active_mode = models.CharField(max_length=50, default="auto")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.role} — {self.conversation}"
