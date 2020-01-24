# Generated by Django 3.0 on 2020-01-23 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20200121_1425'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='launch',
            name='attendance',
        ),
        migrations.AddField(
            model_name='launch',
            name='members_attending',
            field=models.ManyToManyField(related_name='launches_attended', to='home.Account'),
        ),
    ]