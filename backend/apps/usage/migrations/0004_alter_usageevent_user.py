from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("usage", "0003_alter_usageevent_event_type"),
        ("accounts", "0009_alter_impactsurvey_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="usageevent",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="usage_events",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
