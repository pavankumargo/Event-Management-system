# Generated by Django 4.0.3 on 2023-03-14 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0008_events_date_events_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='venue',
            field=models.CharField(default='SRK-221', max_length=30),
        ),
    ]
