# Generated by Django 3.1.4 on 2020-12-03 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0017_auto_20201203_1147'),
    ]

    operations = [
        migrations.RenameField(
            model_name='topic',
            old_name='is_locked',
            new_name='is_lockedd',
        ),
    ]
