# Generated by Django 3.2 on 2021-08-29 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='cart',
            field=models.JSONField(null=True),
        ),
    ]
