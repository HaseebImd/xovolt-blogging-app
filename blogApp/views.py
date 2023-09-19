from django.shortcuts import render, redirect
from django.views import View
from .models import Blogs, MyUser, UserBlogs, Comments
from .decorators import api_login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *

# Create your views here.


class MyHome(View):
    def get(self, request):
        user_blogs = UserBlogs.objects.all().order_by("-id")
        if user := checkUserInSession(request):
            context = {"user_blogs": user_blogs, "user": user}
            return render(request, "home.html", context)
        context = {"user_blogs": user_blogs}
        return render(request, "home.html", context)

class MyBlogs(View):
    def get(self, request):
        if user := checkUserInSession(request):
            context = {"user": user}
            return render(request, "addNewBlog.html", context)
        
    def post(self, request):
        title = request.POST.get("title")
        description = request.POST.get("description")
        images = request.FILES.getlist("headerImage")
        image = images[0] if len(images) != 0 else "None"
        newBlog = Blogs(title=title, description=description,headerImage=image)
        newBlog.save()
        userBlogs = UserBlogs(
            userID=MyUser.objects.get(id=request.session.get("user_id")), blogID=newBlog
        )
        userBlogs.save()
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
        return render(request, "login.html")

    def post(self, request):
        # sourcery skip: remove-unnecessary-else, swap-if-else-branches, use-named-expression
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email, password)
        user = MyUser.objects.filter(email=email, password=password).first()
        if user:
            # If the user exists, store the user's ID in the session
            request.session["user_id"] = user.id
            return redirect("/home")
        else:
            # Handle invalid login credentials, show an error message, or redirect to a login error page
            return render(
                request, "login.html", {"error_message": "Invalid credentials"}
            )


def Logout(request):
    del request.session["user_id"]
    return redirect("/login")


def checkUserInSession(request):
    if user_id := request.session.get("user_id"):
        return MyUser.objects.get(id=user_id)
    else:
        return False


class BlogsDRF(APIView):
    def get(self, request):
        blogs = Blogs.objects.all()
        serializer = BlogSerializer(blogs, many=True)
        return Response({"status": 200, "resp": serializer.data})

    def post(self, request):
        data = request.data
        serializer = BlogSerializer(data=data)
        if not serializer.is_valid():
            return Response(
                {"status": 400, "resp": "Both title and description are required"}
            )
        serializer.save()
        return Response({"status": 200, "resp": serializer.data})

    def patch(self, request):
        try:
            data = request.data
            blog_id = request.GET.get("id", None)

            if blog_id is None:
                return Response(
                    {"status": 400, "resp": "Missing 'id' parameter in URL."}
                )

            blog = Blogs.objects.get(id=blog_id)
            serializer = BlogSerializer(blog, data=data, partial=True)

            if not serializer.is_valid():
                return Response({"status": 400, "resp": serializer.errors})

            serializer.save()

            return Response({"status": 200, "resp": serializer.data})
        except Exception as e:
            return Response({"status": 400, "resp": "Error from exception"})

    def delete(self, request):  # sourcery skip: avoid-builtin-shadow
        try:
            id = request.GET.get("id")
            blog = Blogs.objects.get(id=id)
            blog.delete()
            return Response({"status": 200, "resp": "Blog deleted successfully"})
        except Exception as e:
            return Response({"status": 400, "resp": "Invalid Blog Id"})

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