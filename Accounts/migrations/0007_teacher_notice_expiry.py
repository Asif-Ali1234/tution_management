# Generated by Django 4.1 on 2022-08-30 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accounts', '0006_remove_userauthentication_contact_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='notice_expiry',
            field=models.DateField(blank=True, null=True),
        ),
    ]