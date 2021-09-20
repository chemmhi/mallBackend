from django.shortcuts import render, HttpResponse, Http404
from django.views import View
from io import BytesIO
from utils.create_verify_code import CreateVerifyCode
from user_info.models import UserInfo
import json
import hashlib,time
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
        response['Cache-Control'] = 'no-store, max-age=0'
        print(code)
        return response

class Login(View):
    def post(self, request):
        res = {'status': False, 'data':{}, 'msg':''}
        form = json.loads(request.body.decode('utf-8'))
        userName = form.get('loginUserName')
        password = form.get('pwd')
        loginCode = form.get('loginCode')
        freeLogin = form.get('freeLogin')
        user = UserInfo.objects.filter(userName=userName).values()[0]
        if loginCode.lower() == CHECK_CODE[0].lower():
            if password == user['password']:   #验证码和密码都验证成功
                del user['password']
                del user['sessionId']
                res['status'] = True
                res['data'] = user
                if freeLogin:
                    currentTime = str(time.time())
                    user['c_id'] = loginCode
                    user['t_id'] = currentTime
                    sessionId = hashlib.md5(str(userName + loginCode + currentTime).encode()).hexdigest()
                    UserInfo.objects.filter(userName=userName).update(sessionId=sessionId)
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

class getDetails(View):
    def get(self, request):
        # userName = request.GET.get('userName')
        # user = UserInfo.objects.filter(userName=userName).values()[0]
        response = HttpResponse('ok')
        response['Access-Control-Allow-Origin'] = '*'
        return response
    def post(self,request):
        res = {'status': False, 'data':{}, 'msg':''}
        cookie = json.loads(request.body.decode())
        userName = cookie['UserName']
        c_id = cookie['c_id']
        t_id = cookie['t_id']
        session = hashlib.md5(str(userName+c_id+t_id).encode()).hexdigest()
        try:
            user = UserInfo.objects.filter(userName=userName).values()[0]
            session_id = user['sessionId']
            if session_id == session:
                res['status'] = True
                res['data'] = user
        except Exception as e:
            res['status'] = False
            res['msg'] = ''
        response = HttpResponse(json.dumps(res))
        response['Access-Control-Allow-Origin'] = '*'
        return response
    def options(self, request, *args, **kwargs):
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST,GET, OPTIONS'
        response['Access-Control-Allow-Headers'] = '*'
        # response['Access-Control-Allow-Credentials'] = 'true'
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
            UserInfo.objects.create(
                userName = obj['userName'],
                password= obj['pwd1'],
                phoneNumber= obj['registerPhoneNum'],
            )
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
        response['Access-Control-Allow-Origin'] = 'http://192.168.31.111:8080'
        response['Access-Control-Allow-Credentials'] = 'true'
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