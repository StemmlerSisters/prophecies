# Generated by Django 3.2.6 on 2021-08-30 18:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('actstream', '0003_add_follow_flag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0004_tip'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(blank=True,
                                           choices=[('INFO', 'Info'), ('ERROR', 'Error'), ('SUCCESS', 'Success'),
                                                    ('WARNING', 'Warning')], default='INFO', max_length=7)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('read', models.BooleanField(db_index=True, default=False)),
                ('read_at', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('action', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='actstream.action')),
                ('recipient',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications',
                                   to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('recipient_id', 'action_id')},
            },
        ),
    ]
