# Generated by Django 4.1 on 2022-08-29 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0005_alter_teacher_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userauthentication',
            name='Contact_number',
        ),
        migrations.AlterField(
            model_name='userauthentication',
            name='username',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
