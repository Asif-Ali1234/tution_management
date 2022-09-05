# Generated by Django 4.1 on 2022-08-11 10:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('students', '0003_attendance'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendance',
            name='teacher',
            field=models.ForeignKey(default='pattanasifalikhan@gmail.com', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
