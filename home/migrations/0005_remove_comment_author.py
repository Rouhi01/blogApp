# Generated by Django 5.0.1 on 2024-04-04 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='author',
        ),
    ]
