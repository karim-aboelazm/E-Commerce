# Generated by Django 4.0 on 2022-04-15 09:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='view_count',
        ),
    ]
