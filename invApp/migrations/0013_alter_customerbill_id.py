# Generated by Django 4.0.3 on 2023-05-10 07:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invApp', '0012_alter_customerbill_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerbill',
            name='id',
            field=models.UUIDField(default='7826b4269aab4ab1bfe651f75c61ce84', editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]