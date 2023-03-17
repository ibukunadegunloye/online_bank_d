# Generated by Django 4.1.5 on 2023-03-17 00:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TransferEmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='transfer_email_log', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transfer',
            fields=[
                ('transfer_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('from_account_number', models.CharField(editable=False, max_length=12, null=True)),
                ('to_account_number', models.CharField(editable=False, max_length=12, null=True)),
                ('transfer_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('transfer_date', models.DateTimeField(auto_now_add=True)),
                ('transfer_description', models.CharField(max_length=255, null=True)),
                ('from_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='from_user', to=settings.AUTH_USER_MODEL)),
                ('to_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='to_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreditEmailLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=100)),
                ('body', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_email_log', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Credit',
            fields=[
                ('credit_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('dest_account_number', models.CharField(editable=False, max_length=12, null=True)),
                ('credit_amount', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('credit_source', models.CharField(max_length=50, null=True)),
                ('credit_time', models.DateTimeField(auto_now_add=True)),
                ('credit_description', models.CharField(max_length=255, null=True)),
                ('dest_account', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dest_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreateSavingsAccount',
            fields=[
                ('account_type', models.CharField(default='Savings Account', max_length=255)),
                ('account_number', models.CharField(editable=False, max_length=12, primary_key=True, serialize=False)),
                ('account_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('account_created_at', models.DateTimeField(auto_now_add=True)),
                ('account_updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CreateCurrentAccount',
            fields=[
                ('account_type', models.CharField(default='Current Account', max_length=255)),
                ('account_number', models.CharField(editable=False, max_length=12, primary_key=True, serialize=False)),
                ('account_balance', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('account_created_at', models.DateTimeField(auto_now_add=True)),
                ('account_updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
