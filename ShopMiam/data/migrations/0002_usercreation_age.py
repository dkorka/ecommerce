# Generated by Django 4.1 on 2022-08-27 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercreation',
            name='age',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
