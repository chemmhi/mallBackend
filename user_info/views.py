from django.shortcuts import render, HttpResponse, Http404
from django.views import View
from io import BytesIO
from utils.create_verify_code import CreateVerifyCode
from user_info.models import UserInfo
import json
import hashlib,time
import re
# Create your views here.
PATH = 'static/code.txt'
class VerifyCode(View):
    def get(self, request):
        code = CreateVerifyCode()
        img, code = code.start()
        with open (PATH, 'w') as fp:
            fp.write(code)
        stream = BytesIO()
        img.save(stream, "JPEG")
        response = HttpResponse(stream.getvalue())
        response['Access-Control-Allow-Origin'] = '*'
        response['Content-Type'] = 'image/jpeg'
        response['Cache-Control'] = 'no-store, max-age=0'
        # print(stream.getvalue())
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
        with open(PATH,'r') as fp:
            CHECK_CODE = fp.read()
        if loginCode.lower() == CHECK_CODE.lower():
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

class GetDetails(View):
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
        with open(PATH, 'r') as fp:
            CHECK_CODE = fp.read()
        if obj['registerCode'].lower() == CHECK_CODE.lower():
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
        with open(PATH, 'r') as fp:
            CHECK_CODE = fp.read()
        response = HttpResponse(CHECK_CODE)
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
from django.utils.datastructures import MultiValueDict
class PutProfileImg(View):
    def post(self,request):
        img = request.FILES.get('image')
        userName = request.POST.get('userName')
        imgReG = re.compile('\.([a-zA-Z]+$)')
        imgext = imgReG.search(img.name).group(1)
        imgPath = f'static/profile/img/{userName}.profile.{imgext}'
        with open(imgPath, mode='wb') as f:
            for chunk in img.chunks():
                f.write(chunk)
        UserInfo.objects.filter(userName=userName).update(profileImgUrl=imgPath)
        response = HttpResponse(imgPath)
        response['Access-Control-Allow-Origin'] = '*'
        return response

'''
file = request.FILES.get(“key”)

file 常见的方法有那些？
read() : 把文件读取并放入一个 流中，是一次性读取完成，适合于小图片
chunks() : 以块的方式读取一个文件，适合于 大文件的读取
file 常见的属性有哪些？
name : 文件名
size : 文件大小
content_type : 文件类型
'''