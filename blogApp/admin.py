from django.contrib import admin
from .models import Blogs, MyUser, UserBlogs, Comments

# Register your models here.


class AdminBlog(admin.ModelAdmin):
    list_display = ["title", "createdat"]


class AdminUser(admin.ModelAdmin):
    list_display = ["name", "email", "password", "createdat"]

class AdminUserBlogs(admin.ModelAdmin):
    list_display = ["userID", "blogID", "createdat"]

class AdminComments(admin.ModelAdmin):
    list_display = ["comment", "approved","blogID","userID", "createdat"]

admin.site.register(Blogs, AdminBlog)
admin.site.register(MyUser, AdminUser)
admin.site.register(UserBlogs, AdminUserBlogs)
admin.site.register(Comments, AdminComments)