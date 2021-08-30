from django.shortcuts import render, HttpResponse, Http404
from django.views import View
from io import BytesIO
from utils.create_verify_code import CreateVerifyCode
from user_info.models import UserInfo
import json
# Create your views here.
CHECK_CODE = ['']
class VerifyCode(View):
    def get(self, request):
        code = CreateVerifyCode()
        img, code = code.start()
        CHECK_CODE[0] = code
        stream = BytesIO()
        img.save(stream, "JPEG")
        response = HttpResponse(stream.getvalue())
        response['Access-Control-Allow-Origin'] = '*'
        response['Content-Type'] = 'image/jpeg'
        return response

class Login(View):
    def post(self, request):
        res = {}
        form = json.loads(request.body.decode('utf-8'))
        userName = form.get('loginUserName')
        password = form.get('pwd')
        loginCode = form.get('loginCode')
        user = UserInfo.objects.filter(userName=userName).values()[0]
        if loginCode.lower() == CHECK_CODE[0].lower():
            if password == user['password']:
                del user['password']
                res['status'] = True
                res['data'] = user
            else:
                res['status'] = False
                res['msg'] = '密码错误'
        else:
            res['status'] = False
            res['msg'] = '验证码错误'
        response = HttpResponse(json.dumps(res))
        response['Access-Control-Allow-Origin'] = '*'
        return response
    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST,GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type,X-Request-With,Access-Control-Allow-Origin'
        return response
class Register(View):
    def post(self,request):
        userInfo = {}
        res = {}
        obj = json.loads(request.body.decode('utf-8'))
        if obj['registerCode'].lower() == CHECK_CODE[0].lower():
            userInfo['userName'] = obj['userName']
            userInfo['phoneNumber'] = obj['registerPhoneNum']
            userInfo['password'] = obj['pwd1']
            UserInfo.objects.create(*userInfo)
            res['status'] = True
        else:
            res['status'] = False
            res['msg'] = '验证码错误'
        response = HttpResponse(json.dumps(res))
        response['Access-Control-Allow-Origin'] = '*'
        return response
    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Headers'] = 'application/json'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        response['Access-Control-Allow-Origin'] = '*'
        return response

class Validation(View):
    def post(self, rq):
        result={}
        userName = json.loads(rq.body.decode('utf-8'))['userName']
        queryRes = UserInfo.objects.filter(userName=userName).all()
        result['isExistence'] = True if len(queryRes) > 0 else False
        response = HttpResponse(json.dumps(result))
        response['Access-Control-Allow-Origin'] = '*'
        return response

class GetVerifycode(View):
    def get(self,rq):
        response = HttpResponse(CHECK_CODE[0])
        response['Access-Control-Allow-Origin'] = '*'
        return response


class UpdateCart(View):
    def post(self,request):
        obj = json.loads(request.body.decode('utf-8'))
        userName = obj['userName']
        cart = obj['cart']
        UserInfo.objects.filter(userName=userName).values('cart').update(cart=cart)
        response = HttpResponse(json.dumps('200'))
        response['Access-Control-Allow-Origin'] = '*'
        return response