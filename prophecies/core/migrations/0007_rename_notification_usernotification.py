# Generated by Django 3.2.6 on 2021-09-02 17:34

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('actstream', '0003_add_follow_flag'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0006_merge_0005_auto_20210830_1535_0005_notification'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Notification',
            new_name='UserNotification',
        ),
    ]
