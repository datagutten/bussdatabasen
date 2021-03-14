# Generated by Django 3.1.5 on 2021-03-14 21:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bussdatabase', '0039_forening'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bilde',
            name='bilde',
            field=models.ImageField(upload_to='bussbilder/'),
        ),
        migrations.AlterField(
            model_name='bilde',
            name='buss',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='images', to='bussdatabase.buss'),
        ),
        migrations.AlterField(
            model_name='bilde',
            name='endret_av',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='image_changed', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='bilde',
            name='lagt_til_av',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='images', to=settings.AUTH_USER_MODEL),
        ),
    ]
