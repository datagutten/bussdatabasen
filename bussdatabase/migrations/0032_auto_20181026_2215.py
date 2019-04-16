# Generated by Django 2.1.1 on 2018-10-26 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bussdatabase', '0031_auto_20181026_2152'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selskap',
            name='Se også',
        ),
        migrations.AddField(
            model_name='selskap',
            name='se_ogsa',
            field=models.ManyToManyField(blank=True, db_table='selskap_related', related_name='_selskap_se_ogsa_+', to='bussdatabase.Selskap', verbose_name='Se også'),
        ),
        migrations.AlterField(
            model_name='buss',
            name='chassisprodusent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bussdatabase.Chassisprodusent'),
        ),
        migrations.AlterField(
            model_name='buss',
            name='karosserifabrikk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bussdatabase.Karoserrifabrikk'),
        ),
    ]
