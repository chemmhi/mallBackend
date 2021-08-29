from django.shortcuts import render, HttpResponse
from django.views import View
from io import BytesIO
from utils.create_verify_code import CreateVerifyCode
from user_info.models import UserInfo
import json
# Create your views here.
CHECK_CODE = ['',]
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
        state = request.POST.get('state')
        username = request.POST.get('username')
        print(state,username)
        return HttpResponse('ok')

class Validation(View):
    def post(self,rq):
        result={}
        username = rq.GET.get('username')
        queryRes = UserInfo.objects.filter(userName=username).all()
        result['isExistence'] = True if len(queryRes) > 0 else False
        result['verifyCode'] = CHECK_CODE[0]
        response = HttpResponse(json.dumps(result))
        response['Access-Control-Allow-Origin'] = '*'
        return response

class GetVerifycode(View):
    def get(self,rq):
        response = HttpResponse(CHECK_CODE[0])
        response['Access-Control-Allow-Origin'] = '*'
        return response
