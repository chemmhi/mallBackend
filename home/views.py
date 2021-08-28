from django.shortcuts import render, HttpResponse
from django.views import View
from data_prepare.models import HomeMultidata
from data_prepare.models import HomeGoods
# Create your views here.
class Multidata(View):
    def get(self, request):
        obj = HomeMultidata.objects.filter(id=1).values('home_multidata')
        response = HttpResponse(obj[0]['home_multidata']) if len(obj) != 0 else {}
        response['Access-Control-Allow-Origin'] = '*'
        return response

class Data(View):
    def get(self, request):
        type = request.GET.get('type')
        page = request.GET.get('page')
        res = HomeGoods.objects.filter(type=type, page=page).values('content')
        response = HttpResponse(res[0]['content']) if len(res)!=0 else {}
        response['Access-Control-Allow-Origin'] = '*'
        return response