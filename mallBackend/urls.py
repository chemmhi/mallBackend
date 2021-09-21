"""mallBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles import views
from django.urls import path, include, re_path
from details import views as views_get_details
from category import views as views_category


urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', include('home.urls')),
    path('detail/', views_get_details.GetDetails.as_view()),
    path('recommend/', views_get_details.GetRecommend.as_view()),
    path('category/', views_category.GetCategory.as_view()),
    re_path('subcategory/$', views_category.GetSubcategory.as_view()),
    path('subcategory/detail/', views_category.GetSubcategoryDetail.as_view()),
    path('data_prepare/', include('data_prepare.urls')),
    path('user/', include('user_info.urls')),
]
