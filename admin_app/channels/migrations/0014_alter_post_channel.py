# Generated by Django 5.1.4 on 2025-01-15 12:52

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0013_remove_channel_last_scanned_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='channels.channel', verbose_name='Канал'),
        ),
    ]
