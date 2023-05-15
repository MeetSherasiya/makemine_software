# Generated by Django 4.0.3 on 2023-05-09 20:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0009_alter_customerbill_id_alter_invoiceitem_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerbill',
            name='id',
            field=models.UUIDField(default=uuid.UUID('f824f2f0-7dc3-440c-aa1b-16dc64710e37'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='invoiceitem',
            name='id',
            field=models.UUIDField(default=uuid.UUID('b1419c7b-db4a-4a53-9a49-715c31588261'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='product',
            name='id',
            field=models.UUIDField(default=uuid.UUID('15b21f79-eb86-4e71-bf67-48da27f2b38c'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='stockhistory',
            name='id',
            field=models.UUIDField(default=uuid.UUID('98cf1ee9-50c0-4449-8cb4-410df944d6ed'), editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='tempitem',
            name='id',
            field=models.UUIDField(default=uuid.UUID('f2514cf2-521c-4cf2-880c-3d6052833964'), editable=False, primary_key=True, serialize=False),
        ),
    ]