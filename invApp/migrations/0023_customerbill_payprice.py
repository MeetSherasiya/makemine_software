# Generated by Django 4.1.6 on 2023-05-31 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0022_customerbill_per_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='payprice',
            field=models.IntegerField(default=0),
        ),
    ]