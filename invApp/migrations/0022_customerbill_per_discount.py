# Generated by Django 4.1.6 on 2023-05-31 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0021_customerbill_discount_alter_invoiceitem_itemsize_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='per_discount',
            field=models.IntegerField(default=0),
        ),
    ]
