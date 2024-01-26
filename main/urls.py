"""root URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('librarystaff', views.LibrarystaffProfileViewSet,
                basename='librarystaff'),
router.register('bookcategory', views.BookCategoryViewSet,
                basename='bookcategory'),
router.register('publisher', views.PublisherViewSet, basename='publisher'),
router.register('books', views.BookViewset, basename='books')
urlpatterns = [
    path('signup', views.SignupAPI.as_view()),
    path('login', views.LoginAPI.as_view()),
    path('admin', views.AdminLoginAPI.as_view()),
]+router.urls
