# Generated by Django 4.1.6 on 2023-05-15 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0018_customerbill_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.CharField(default='10mm', max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]