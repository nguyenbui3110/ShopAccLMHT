# Generated by Django 4.1.7 on 2023-04-16 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_accgame_image_alter_accgame_image1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accgame',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%(name)s/'),
        ),
        migrations.AlterField(
            model_name='accgame',
            name='image1',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%(name)s/'),
        ),
        migrations.AlterField(
            model_name='accgame',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%(name)s/'),
        ),
        migrations.AlterField(
            model_name='accgame',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/%(name)s/'),
        ),
    ]