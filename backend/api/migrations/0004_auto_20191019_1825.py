# Generated by Django 2.2.4 on 2019-10-19 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20190829_0416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='searched_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]