from django.shortcuts import render, HttpResponse
from django.views import View
from data_prepare.models import HomeMultidata
from data_prepare.models import HomeGoods
from data_prepare.models import Details, Redommend

import requests
import json
# Create your views here.

#获取数据并保存到数据库中
class GetHomeMultidata(View):
    def get(self, request):
        if(len(HomeMultidata.objects.all()) ==  0):
            res = requests.get('http://152.136.185.210:7878/api/m5/home/multidata')
            HomeMultidata.objects.create(home_multidata=res.text)
        return HttpResponse('ok')

class GetHomeData(View):
    def get(self, request):
        def downloadData(type, page):
            try:
                res = requests.get(url,params={'type':type, 'page':page})
                if(res.text != 0):
                    # HomeGoods.objects.create(page=page, type=type, content=res.text)
                    page +=1
                    for item in json.loads(res.text)['data']['list']:
                        iid = item['iid']
                        print(iid)
                        obj = requests.get('http://152.136.185.210:7878/api/m5/detail', params={'iid':iid})
                        Details.objects.create(iid=iid, goods=obj.text)
                return downloadData(type, page)
            except Exception as e:
                print(e)
                return list, page
        def get_goods(type):
            li, total_page = downloadData(type, 1)
            return (type, li, total_page)
        if (True):
            url = 'http://152.136.185.210:7878/api/m5/home/data'
            get_goods('pop')
            get_goods('new')
            get_goods('sell')
        return HttpResponse('ok')


class GetRecommend(View):
    def get(self, request):
        res = requests.get('http://152.136.185.210:7878/api/m5/recommend')
        Redommend.objects.create(recommend= res.text)
        return HttpResponse('ok')