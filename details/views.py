from django.shortcuts import render, HttpResponse
from django.views import View
from data_prepare.models import Details, Redommend
# Create your views here.
class GetDetails(View):
    def get(self,request):
        iid = request.GET.get('iid')
        obj = Details.objects.filter(iid = iid).values('goods')
        response = HttpResponse(obj[0]['goods'])
        response['Access-Control-Allow-Origin'] = '*'
        return response

class GetRecommend(View):
    def get(self, request):
        obj = Redommend.objects.filter(id=1).values('recommend')
        response = HttpResponse(obj[0]['recommend'])
        response['Access-Control-Allow-Origin'] = '*'
        return response