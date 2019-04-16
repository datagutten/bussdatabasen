# Generated by Django 2.1 on 2018-08-17 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bussdatabase', '0007_auto_20180817_1154'),
    ]

    operations = [
        migrations.AddField(
            model_name='buss',
            name='tilstand',
            field=models.CharField(blank=True, choices=[(1, 'Helrestaurert'), (2, 'Oppusset'), (3, 'Urestaurert'), (4, 'Under restaurering'), (5, 'Hensatt'), (6, 'Ombygget'), (7, 'Avskiltet'), (8, 'Hogget'), (9, 'Solgt til utlandet'), (None, 'Ikke oppgitt')], max_length=50, null=True),
        ),
    ]
