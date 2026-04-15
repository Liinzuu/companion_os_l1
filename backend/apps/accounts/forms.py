"""
Accounts app — Forms.

Why UserCreationForm as the base?
Django's UserCreationForm already handles:
- password confirmation (type it twice, must match)
- password strength validation
- duplicate username check

We extend it to add our custom fields (language, voice preference).
Writing this from scratch would mean reimplementing all of that.
"""
from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import InviteCode, User


class RegisterForm(UserCreationForm):
    """
    Registration form for new Companion OS users.

    Requires a valid invite code. No code = no account.
    This protects vulnerable users by controlling who has access
    during early testing and beyond.
    """

    invite_code = forms.CharField(
        max_length=40,
        label="Invite code",
        help_text="You need an invite code to create an account.",
    )

    class Meta:
        model = User
        fields = [
            "invite_code",
            "username",
            "password1",
            "password2",
        ]

    def clean_invite_code(self):
        """Validate the invite code exists and is still usable."""
        code = self.cleaned_data.get("invite_code", "").strip()
        try:
            invite = InviteCode.objects.get(code=code)
        except InviteCode.DoesNotExist:
            raise forms.ValidationError("This invite code is not valid.")

        if not invite.is_valid:
            raise forms.ValidationError("This invite code has already been used.")

        # Store the invite object so the view can mark it as used after save
        self._invite = invite
        return code
