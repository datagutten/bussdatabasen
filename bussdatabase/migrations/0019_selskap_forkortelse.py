# Generated by Django 2.1 on 2018-08-24 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bussdatabase', '0018_auto_20180823_2023'),
    ]

    operations = [
        migrations.AddField(
            model_name='selskap',
            name='forkortelse',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
