# Migration for InviteCode model — access control for registration

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="InviteCode",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "code",
                    models.CharField(
                        default=uuid.uuid4,
                        help_text="The invite code users enter during registration.",
                        max_length=40,
                        unique=True,
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        help_text="Who is this code for? e.g. 'Niina testing', 'Jon demo'",
                        max_length=100,
                    ),
                ),
                (
                    "max_uses",
                    models.PositiveIntegerField(
                        default=1,
                        help_text="How many times this code can be used. 0 = unlimited.",
                    ),
                ),
                (
                    "times_used",
                    models.PositiveIntegerField(default=0),
                ),
                (
                    "is_active",
                    models.BooleanField(default=True),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True),
                ),
            ],
        ),
    ]
