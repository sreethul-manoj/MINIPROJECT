# Generated by Django 5.2 on 2025-07-07 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Mobile_number',
            field=models.CharField(default=2, max_length=50),
            preserve_default=False,
        ),
    ]
