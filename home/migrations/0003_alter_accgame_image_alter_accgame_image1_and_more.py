# Generated by Django 4.1.7 on 2023-04-16 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_accgame_image1'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accgame',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%(slug)s/'),
        ),
        migrations.AlterField(
            model_name='accgame',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%(slug)s/'),
        ),
        migrations.AlterField(
            model_name='accgame',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%(slug)s/'),
        ),
        migrations.AlterField(
            model_name='accgame',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%(slug)s/'),
        ),
    ]
