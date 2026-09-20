from django.db import migrations


DEFAULTS = [
    ("load_created", True, False),
    ("payment_updated", True, True),
    ("application_received", True, True),
    ("expense_added", True, False),
    ("settlement_created", True, False),
    ("doc_expiring", True, True),
]


def seed(apps, schema_editor):
    Rule = apps.get_model("operations", "NotificationRule")
    for event, in_app, email in DEFAULTS:
        Rule.objects.get_or_create(event=event, defaults={"in_app": in_app, "email": email})


def unseed(apps, schema_editor):
    apps.get_model("operations", "NotificationRule").objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("operations", "0005_notificationrule_company_address_company_ein_and_more")]
    operations = [migrations.RunPython(seed, unseed)]
