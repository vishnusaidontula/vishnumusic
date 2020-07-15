# Generated by Django 3.0.4 on 2020-07-14 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0007_auto_20190126_1926'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='type',
            field=models.CharField(choices=[('ty1', 'public'), ('ty2', 'private')], default='public', max_length=50),
        ),
        migrations.AddField(
            model_name='song',
            name='type',
            field=models.CharField(choices=[('ty1', 'public'), ('ty2', 'private')], default='public', max_length=50),
        ),
    ]
