# Author: Chenchen

from django.urls import path
from data_prepare import views
urlpatterns = [
    # path('home/data/', views.GetHomeData.as_view()),
    # path('home/multidata/', views.GetHomeMultidata.as_view()),
    # path('recommend/', views.GetRecommend.as_view()),
    path('category/', views.GetCategory.as_view()),
]
