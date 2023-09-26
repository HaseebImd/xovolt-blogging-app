from django.shortcuts import render, redirect
from django.views import View
from .utils import send_new_blog_notification
from .models import Blogs, MyUser, UserBlogs, Comments
from .decorators import api_login_required
from django.http import JsonResponse
from django.contrib.auth.models import User
from functools import wraps
from .models import *
from .utils import send_new_blog_notification
import asyncio
from asgiref.sync import async_to_sync, sync_to_async
from django.utils.decorators import method_decorator
from django.db import transaction
# Create your views here.


class MyHome(View):
    def get(self, request):
        if user := checkUserInSession(request):
        # Get a list of unique categories with associated blogs
            categories_with_blogs = Category.objects.filter(blogcategory__isnull=False).distinct()

            # Create a dictionary to store categorized blogs
            categorized_blogs = {}

            for category in categories_with_blogs:
                # Get blog IDs associated with the current category
                blog_ids = BlogCategory.objects.filter(categoryID=category).values_list('blogID', flat=True)

                # Fetch the blogs associated with these IDs
                blogs = Blogs.objects.filter(id__in=blog_ids)

                categorized_blogs[category] = blogs

            context = {
                'categorized_blogs': categorized_blogs,
                'user': user,
            }
            return render(request, "home.html", context)            # user_blogs = UserBlogs.objects.all().order_by("-id")
            # if user := checkUserInSession(request):
            #     context = {"user_blogs": user_blogs, "user": user}
            #     return render(request, "home.html", context)
            # context = {"user_blogs": user_blogs}
            # return render(request, "home.html", context)
        else:
            return redirect("/login")

class MyBlogs(View):
    def get(self, request):
        categories=Category.objects.all()
        if user := checkUserInSession(request):
            context = {"user": user,"categories":categories}
            return render(request, "addNewBlog.html", context)
        else:
            return redirect("/login")
    def post(self, request):
        title = request.POST.get("title")
        description = request.POST.get("description")
        images = request.FILES.getlist("headerImage")
        image = images[0] if len(images) != 0 else "None"
        newBlog = Blogs(title=title, description=description,headerImage=image)
        newBlog.save()
        send_new_blog_notification(newBlog.title)
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        blog_category = BlogCategory(blogID=newBlog, categoryID=category)
        blog_category.save()
        if request.session.get("admin"):
            return redirect("/home")

        if user_id := request.session.get("user_id"):
            user = MyUser.objects.get(id=user_id)
            user_blogs = UserBlogs(userID=user, blogID=newBlog)
            user_blogs.save()

        return redirect("/home") 
        

    def delete(self, request):  # sourcery skip: avoid-builtin-shadow
        id = request.GET.get("id")
        blog = Blogs.objects.get(id=id)
        blog.delete()
        return redirect("/home")

@api_login_required
def AddNewBlog(request):
    if user := checkUserInSession(request):
        context = {"user": user}
    return render(request, "addNewBlog.html", context)


@api_login_required
def DeleteBlog(request, id):
    blog = Blogs.objects.get(id=id)
    blog.delete()
    return redirect("/home")


@api_login_required
def BlogDetails(request, id):
    blog = Blogs.objects.get(id=id)
    comments=Comments.objects.filter(blogID=blog, approved=True)
    if user := checkUserInSession(request):
        context = {"blog": blog, "user": user,"comments":comments}
        return render(request, "blogDetails.html", context)
    context = {"blog": blog,"comments":comments}
    return render(request, "blogDetails.html", context)


@api_login_required
def EditBlog(request, id):  # sourcery skip: extract-method
    blog = Blogs.objects.get(id=id)
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        blog.title = title
        blog.description = description
        blog.save()
        return redirect("/home")
    if user_id := request.session.get("user_id"):
        user = MyUser.objects.get(id=user_id)
        context = {"blog": blog, "user": user}
    return render(request, "editBlog.html", context)


class SignUp(View):
    def get(self, request):
        if user := checkUserInSession(request):
            return redirect('/home')
        
        return render(request, "signup.html")
        
        

    def post(self, request):
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        images = request.FILES.getlist("images")
        image = images[0] if len(images) != 0 else "None"
        if MyUser.objects.filter(email=email).exists():
            # You can return an error message or redirect the user to an error page
            return render(
                request, "signup.html", {"error_message": "Email already registered."}
            )
        # Create the new user if the email is not registered
        newUser = MyUser(name=name, email=email, password=password, userImage=image)
        newUser.save()
        return redirect("/login")


class Login(View):
    def get(self, request):
        if user := checkUserInSession(request):
            return redirect('/home')
        return render(request, "login.html")
        

    def post(self, request):  # sourcery skip: use-named-expression
        email = request.POST.get("email")
        password = request.POST.get("password")
        my_user = MyUser.objects.filter(email=email, password=password).first()
        if my_user:
            request.session["user_id"] = my_user.id
            request.session["admin"] = False
            return redirect("/home")
        else:
            print("checking from user table")
            # If the user is not found in the MyUser table, try to find them in the User table
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                # If the user is found in the User table and the password is correct, log them in
                request.session["user_id"] = user.id
                request.session["admin"] = True
                return redirect("/home")

        # Handle invalid login credentials, show an error message, or redirect to a login error page
        return render(
            request, "login.html", {"error_message": "Invalid credentials"}
        )


def Logout(request):
    del request.session["user_id"]
    return redirect("/login")


def checkUserInSession(request):
    if user_id := request.session.get("user_id"):
        if admin := request.session.get("admin"):
            return User.objects.get(id=user_id)
        return MyUser.objects.get(id=user_id)
    else:
        return False

# CRUD Functionality using DRF

@api_login_required
def AddNewComment(request):
    if request.method == "POST":
        blogID = request.POST.get("blogid")
        userID = request.session.get("user_id")
        comment = request.POST.get("comment")
        newComment = Comments(
            blogID=Blogs.objects.get(id=blogID),
            userID=MyUser.objects.get(id=userID),
            comment=comment,
        )
        newComment.save()
        return redirect(f"/blog-details/{blogID}")
    

@api_login_required
def CommentSection(request):
    if request.method == "GET":
        comments=Comments.objects.all().order_by("-id")
        if user := checkUserInSession(request):
            context = {"comments": comments, "user": user}
            return render(request, "comments.html", context)
        

def ApproveComment(request):
    if request.method == 'GET':
        comment_id = request.GET.get('comment_id')
        try:
            comment = Comments.objects.get(pk=comment_id)
            comment.approved = not comment.approved
            comment.save()
            response_data = {
                'message': 'Comment approval toggled successfully',
            }
            return JsonResponse(response_data)
        except Comments.DoesNotExist:
            error_message = 'Comment not found with ID ' + comment_id
            response_data = {
                'error': error_message,
            }
            return JsonResponse(response_data, status=404)
        except Exception as e:
            error_message = 'An error occurred: ' + str(e)
            response_data = {
                'error': error_message,
            }
            return JsonResponse(response_data, status=500)
