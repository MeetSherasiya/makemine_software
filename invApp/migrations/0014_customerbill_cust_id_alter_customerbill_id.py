# Generated by Django 4.0.3 on 2023-05-10 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0013_alter_customerbill_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='cust_id',
            field=models.UUIDField(default='9cac33bfb9ed4d13b4edcd06e1bb1b1b', editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='customerbill',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
