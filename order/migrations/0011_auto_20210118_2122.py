# Generated by Django 3.1.4 on 2021-01-18 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0010_order_mode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Preparing', 'Preparing'), ('On Shipping', 'On Shipping'), ('Completed', 'Completed'), ('Canceled', 'Canceled'), ('Return Requested', 'Return Requested'), ('Returned', 'Returned')], default='New', max_length=50),
        ),
    ]