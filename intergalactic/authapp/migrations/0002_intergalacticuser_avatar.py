# Generated by Django 3.1.7 on 2021-04-04 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='intergalacticuser',
            name='avatar',
            field=models.ImageField(blank=True, upload_to='users_avatars'),
        ),
    ]