# Generated by Django 4.1.5 on 2023-01-30 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bank', '0004_alter_savings_account_account_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='savings_account',
            name='savings_rubbish',
            field=models.CharField(max_length=30),
        ),
    ]