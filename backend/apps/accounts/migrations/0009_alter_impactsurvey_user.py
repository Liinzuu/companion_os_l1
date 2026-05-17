from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0008_partnershipinquiry"),
    ]

    operations = [
        migrations.AlterField(
            model_name="impactsurvey",
            name="user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="impact_surveys",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
