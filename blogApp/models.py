from django.db import models
from tinymce import models as tinymce_models

# Create your models here.
class Blogs(models.Model):
    title = models.CharField(max_length=200)
    description =tinymce_models.HTMLField()
    headerImage   =models.ImageField(upload_to='upload/blogs/',null=True, default=None)
    createdat = models.DateTimeField(
        db_column='createdAt', blank=True, null=True, auto_now_add=True)
    updatedat = models.DateTimeField(
        db_column='updatedAt', blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name_plural = "Blogs"

    def __str__(self):
        return self.title
    

class MyUser(models.Model):
    name            =models.CharField(max_length=200)
    email           =models.EmailField(max_length=200)
    userImage       =models.ImageField(upload_to='upload/users/')
    password        =models.CharField(max_length=200)
    createdat       =models.DateTimeField(db_column='createdAt', blank=True, null=True, auto_now_add=True)
    updatedat       =models.DateTimeField(db_column='updatedAt', blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name_plural = "Users"

    def __str__(self):
        return self.name
    

class UserBlogs(models.Model):
    
    userID = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    blogID = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    createdat = models.DateTimeField(
        db_column='createdAt', blank=True, null=True, auto_now_add=True)
    updatedat = models.DateTimeField(
        db_column='updatedAt', blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name_plural = "Users Blogs"


class Comments(models.Model):
    blogID = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    userID = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment = models.TextField()
    approved = models.BooleanField(default=False)
    createdat = models.DateTimeField(
        db_column='createdAt', blank=True, null=True, auto_now_add=True)
    updatedat = models.DateTimeField(
        db_column='updatedAt', blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.comment
    


class Category(models.Model):
    category = models.CharField(max_length=200, unique=True)
    createdat = models.DateTimeField(
        db_column='createdAt', blank=True, null=True, auto_now_add=True)
    updatedat = models.DateTimeField(
        db_column='updatedAt', blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category
    

class BlogCategory(models.Model):
    blogID = models.ForeignKey(Blogs, on_delete=models.CASCADE)
    categoryID = models.ForeignKey(Category, on_delete=models.CASCADE)
    createdat = models.DateTimeField(
        db_column='createdAt', blank=True, null=True, auto_now_add=True)
    updatedat = models.DateTimeField(
        db_column='updatedAt', blank=True, null=True, auto_now=True)

    class Meta:
        verbose_name_plural = "Blog Categories"