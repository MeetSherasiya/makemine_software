# Generated by Django 4.0.3 on 2023-05-10 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0017_alter_customerbill_id_alter_invoiceitem_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customerbill',
            name='payment',
            field=models.CharField(choices=[('1', 'Cash'), ('2', 'Online'), ('3', 'Pending')], default=1, max_length=2),
        ),
    ]