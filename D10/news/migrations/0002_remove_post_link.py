# Generated by Django 3.1.2 on 2020-11-02 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='link',
        ),
    ]