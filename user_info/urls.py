# Author: Chenchen

from django.urls import path,re_path
from user_info import views

urlpatterns = [
    path('verifycode/img/',views.VerifyCode.as_view()),
    path('login/',views.Login.as_view()),
    path('register/',views.Register.as_view()),
    path('updatecart/',views.UpdateCart.as_view()),
    path('username/validation/',views.Validation.as_view()),   #验证用户名是否可用
    path('getverifycode/',views.GetVerifycode.as_view()),   #获取验证码
    path('getDetails/',views.getDetails.as_view()),   #获取验证码
]