# Generated by Django 3.1.7 on 2021-04-07 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='chest',
            field=models.PositiveSmallIntegerField(default=1, max_length=3, verbose_name='obwód klatki'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manager',
            name='chest',
            field=models.PositiveSmallIntegerField(default='1', max_length=3, verbose_name='obwód klatki'),
            preserve_default=False,
        ),
    ]
