# Generated by Django 4.2.2 on 2023-09-18 08:14

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0002_alter_blogs_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='description',
            field=tinymce.models.HTMLField(),
        ),
    ]
