# Generated by Django 2.2.4 on 2020-11-03 20:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inApp', '0002_client_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='client',
            old_name='state',
            new_name='city',
        ),
    ]
