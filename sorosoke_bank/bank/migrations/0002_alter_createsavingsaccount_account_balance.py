# Generated by Django 4.1.5 on 2023-03-21 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createsavingsaccount',
            name='account_balance',
            field=models.DecimalField(decimal_places=2, default=1000000.0, max_digits=20),
        ),
    ]
