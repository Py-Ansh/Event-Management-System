# Generated by Django 5.0.6 on 2024-05-30 07:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Events', '0003_event_completed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='completed',
        ),
    ]