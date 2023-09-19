# Generated by Django 4.2.2 on 2023-09-18 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogApp', '0004_remove_blogs_date_blogs_createdat_blogs_updatedat'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=200)),
                ('userImage', models.ImageField(upload_to='upload/users/')),
                ('password', models.CharField(max_length=200)),
                ('createdat', models.DateTimeField(auto_now_add=True, db_column='createdAt', null=True)),
                ('updatedat', models.DateTimeField(auto_now=True, db_column='updatedAt', null=True)),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
    ]