# Generated by Django 5.0.6 on 2024-09-20 16:05

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('siteDeclaracao', '0013_alter_temporarypagedata_attempt_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pagerelationship',
            name='DataUserPayment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='page_relationship', to='siteDeclaracao.datauserpayment'),
        ),
        migrations.AlterField(
            model_name='temporarypagedata',
            name='attempt_id',
            field=models.CharField(default=uuid.UUID('7380eadc-c41d-49d5-8052-c2f0f5df28e5'), max_length=200, unique=True),
        ),
    ]
