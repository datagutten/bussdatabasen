# Generated by Django 2.1 on 2018-08-23 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bussdatabase', '0017_auto_20180822_1204'),
    ]

    operations = [
        migrations.AddField(
            model_name='karoserrifabrikk',
            name='alternativt_navn',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='karoserrifabrikk',
            name='antall',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='karoserrifabrikk',
            name='forkortelse',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='karoserrifabrikk',
            name='første_år',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='karoserrifabrikk',
            name='rutebil_nr',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='karoserrifabrikk',
            name='siste_år',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='karoserrifabrikk',
            name='wikipedia',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='selskap',
            name='wikipedia',
            field=models.URLField(blank=True, null=True),
        ),
    ]
