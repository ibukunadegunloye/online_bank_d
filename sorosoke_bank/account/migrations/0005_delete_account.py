# Generated by Django 4.1.5 on 2023-01-30 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_account_account_number'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Account',
        ),
    ]