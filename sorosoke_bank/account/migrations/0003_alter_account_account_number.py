# Generated by Django 4.1.5 on 2023-01-27 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_account_account_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_number',
            field=models.PositiveBigIntegerField(),
        ),
    ]
