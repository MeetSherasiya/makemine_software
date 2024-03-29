# Generated by Django 4.1.6 on 2023-05-31 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0020_invoiceitem_itemsize_stockhistory_itemsize_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='itemsize',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='size',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='itemsize',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='tempitem',
            name='tempsize',
            field=models.CharField(max_length=50),
        ),
    ]
