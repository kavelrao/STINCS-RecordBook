# Generated by Django 3.0 on 2019-12-16 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20191215_2005'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='join_code',
            field=models.CharField(default=77777777, max_length=8),
            preserve_default=False,
        ),
    ]
