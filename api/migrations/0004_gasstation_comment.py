# Generated by Django 3.2.23 on 2025-02-04 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_gasstation_map_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='gasstation',
            name='comment',
            field=models.CharField(default='Not Found', max_length=10),
        ),
    ]
