# Generated by Django 4.2.2 on 2023-09-20 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0002_blogcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogs',
            name='category',
            field=models.CharField(default='General', max_length=200, null=True),
        ),
        migrations.DeleteModel(
            name='BlogCategory',
        ),
    ]