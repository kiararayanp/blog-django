from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("profile", views.profile, name="profile"),
    path("login", views.login_page, name="login"),
    path("register", views.register, name="register"),
    path("logout", views.logout_user, name="logout"),
    path("blog/<int:pk>", views.blog_single, name="blog_single"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path("edit_blog/<int:pk>", views.edit_blog, name="edit_blog"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("error", views.error_page, name="error"),
]
