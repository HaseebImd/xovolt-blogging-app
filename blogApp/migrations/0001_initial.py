# Generated by Django 4.2.2 on 2023-09-20 08:52

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', tinymce.models.HTMLField()),
                ('headerImage', models.ImageField(default=None, null=True, upload_to='upload/blogs/')),
                ('createdat', models.DateTimeField(auto_now_add=True, db_column='createdAt', null=True)),
                ('updatedat', models.DateTimeField(auto_now=True, db_column='updatedAt', null=True)),
            ],
            options={
                'verbose_name_plural': 'Blogs',
            },
        ),
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
        migrations.CreateModel(
            name='UserBlogs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('createdat', models.DateTimeField(auto_now_add=True, db_column='createdAt', null=True)),
                ('updatedat', models.DateTimeField(auto_now=True, db_column='updatedAt', null=True)),
                ('blogID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogApp.blogs')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogApp.myuser')),
            ],
            options={
                'verbose_name_plural': 'Users Blogs',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('approved', models.BooleanField(default=False)),
                ('createdat', models.DateTimeField(auto_now_add=True, db_column='createdAt', null=True)),
                ('updatedat', models.DateTimeField(auto_now=True, db_column='updatedAt', null=True)),
                ('blogID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogApp.blogs')),
                ('userID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blogApp.myuser')),
            ],
            options={
                'verbose_name_plural': 'Comments',
            },
        ),
    ]
