# Generated by Django 3.1.1 on 2020-12-30 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userprofile_pincode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='Users/profile.png', upload_to='images/users/'),
        ),
    ]
