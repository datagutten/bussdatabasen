# Generated by Django 2.1 on 2018-08-22 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bussdatabase', '0014_auto_20180818_1833'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navn', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Tilstand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('navn', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='bilde',
            name='bildetekst',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='bilde',
            name='kreditering',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
