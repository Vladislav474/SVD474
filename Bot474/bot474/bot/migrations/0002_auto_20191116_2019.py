# Generated by Django 2.2 on 2019-11-16 17:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Materials',
            new_name='Material',
        ),
        migrations.RenameModel(
            old_name='Themes',
            new_name='Theme',
        ),
    ]
