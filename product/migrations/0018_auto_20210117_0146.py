# Generated by Django 3.1.4 on 2021-01-16 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0017_auto_20210117_0145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='start',
            field=models.DateField(),
        ),
    ]
