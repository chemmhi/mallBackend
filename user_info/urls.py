# Author: Chenchen

from django.urls import path
from user_info import views

urlpatterns = [
    path('verifycode/img/',views.VerifyCode.as_view()),
    path('login/',views.Login.as_view()),
    path('username/validation/',views.Validation.as_view()),   #验证用户名是否可用
    path('getverifycode/',views.GetVerifycode.as_view()),   #获取验证码
]