# Generated by Django 4.2.4 on 2023-09-14 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0023_customerbill_payprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='custemail',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
