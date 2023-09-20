from django.contrib import admin
from .models import Blogs, MyUser, UserBlogs, Comments, Category, BlogCategory

# Register your models here.


class AdminBlog(admin.ModelAdmin):
    list_display = ["title", "createdat"]
    list_filter = ("createdat",)  # Add filtering by category
    search_fields = ["title", "description"]  # Add search by title and description


class AdminUser(admin.ModelAdmin):
    list_display = ["name", "email", "password", "createdat"]

class AdminUserBlogs(admin.ModelAdmin):
    list_display = ["userID", "blogID", "createdat"]

class AdminComments(admin.ModelAdmin):
    list_display = ["comment", "approved","blogID","userID", "createdat"]


class AdminCategory(admin.ModelAdmin):
    list_display = ["category", "createdat"]


class AdminBlogCategory(admin.ModelAdmin):
    list_display = ["blogID","categoryID", "createdat"]


admin.site.register(Blogs, AdminBlog)
admin.site.register(MyUser, AdminUser)
admin.site.register(UserBlogs, AdminUserBlogs)
admin.site.register(Comments, AdminComments)
admin.site.register(Category, AdminCategory)
admin.site.register(BlogCategory, AdminBlogCategory)
