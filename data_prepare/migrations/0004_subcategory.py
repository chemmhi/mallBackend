# Generated by Django 3.2 on 2021-08-28 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_prepare', '0003_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subcategory', models.JSONField()),
                ('maitKey', models.CharField(max_length=15)),
            ],
        ),
    ]