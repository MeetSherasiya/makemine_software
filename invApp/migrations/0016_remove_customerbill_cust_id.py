# Generated by Django 4.0.3 on 2023-05-10 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0015_alter_customerbill_cust_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customerbill',
            name='cust_id',
        ),
    ]
