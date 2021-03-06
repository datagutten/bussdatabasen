# Generated by Django 2.1 on 2018-08-22 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bussdatabase', '0016_auto_20180822_0944'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='status',
            options={'verbose_name_plural': 'statuser'},
        ),
        migrations.AlterModelOptions(
            name='tilstand',
            options={'verbose_name_plural': 'tilstander'},
        ),
        migrations.AddField(
            model_name='buss',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bussdatabase.Status'),
        ),
        migrations.AlterField(
            model_name='buss',
            name='tilstand',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bussdatabase.Tilstand'),
        ),
    ]
