# Generated by Django 4.1.5 on 2023-01-30 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savings_account',
            name='account_number',
            field=models.PositiveBigIntegerField(default=1675098862, primary_key=True, serialize=False),
        ),
    ]
