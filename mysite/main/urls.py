#Here we define the paths to our different web pages
from django.urls import path
from . import views

urlpatterns = [ 
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login_view"),
    path("listings/", views.listings_view, name="listings_view"),
    path("mainpage/", views.main_page, name="main_page")
    ]
