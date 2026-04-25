"""
Data migration: ensure the singleton SystemConfig row exists.

Why: the kill switch URL (/admin/safety/systemconfig/1/change/) requires
pk=1 to exist. Without this row, the operator's bookmark would 404 and
they would have to manually click "Add" before the switch becomes usable.
That is friction we cannot afford during an emergency.

Idempotent: get_or_create makes this safe to run on existing databases.
Reversal is intentionally a no-op — rolling back the migration must not
delete the kill switch row.
"""
from django.db import migrations


def create_default_systemconfig(apps, schema_editor):
    SystemConfig = apps.get_model("safety", "SystemConfig")
    SystemConfig.objects.get_or_create(
        pk=1,
        defaults={"maintenance_mode": False},
    )


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("safety", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_systemconfig, noop),
    ]
