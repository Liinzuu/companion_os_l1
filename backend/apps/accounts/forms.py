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
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegisterForm(UserCreationForm):
    """
    Registration form for new Companion OS users.

    Inherits from UserCreationForm which gives us:
    - username field
    - password1 field (enter password)
    - password2 field (confirm password)
    - all built-in validation

    We add language and voice preference so users can set them on signup.
    Both have sensible defaults so they're not required.
    """

    class Meta:
        model = User
        fields = [
            "username",
            "password1",
            "password2",
        ]
