# Generated by Django 3.2 on 2021-09-20 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_info', '0003_userinfo_sessionid'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='profileImgUrl',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
