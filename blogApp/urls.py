from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from blogApp import views
from blogApp.views import Blogs, SignUp, Login, MyBlogs,MyHome
urlpatterns = [
    
    path('', SignUp.as_view(),),
    path('login', Login.as_view(),name="login"),
    path('home', MyHome.as_view(),),
    path('blogs', MyBlogs.as_view(),name="blogs"),
    path('blog-details/<int:id>', views.BlogDetails, name="BlogDetails"),
    path('delete-blog/<int:id>', views.DeleteBlog, name="DeleteBlog"),
    path('edit-blog/<int:id>', views.EditBlog, name="EditBlog"),
    path('logout', views.Logout, name="Logout"),
    
    # Comment Section
    path('add-new-comment', views.AddNewComment, name="AddNewComment"),
    path('comment-section', views.CommentSection, name="CommentSection"),
    path('approve-comment', views.ApproveComment, name="ApproveComment"),


]
if settings.DEBUG:  
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  