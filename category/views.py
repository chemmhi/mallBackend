from django.shortcuts import render, HttpResponse
from django.views import View
from data_prepare.models import Category, Subcategory, SubcategoryDetail
# Create your views here.
class GetCategory(View):
    def get(self,request):
        res = Category.objects.filter(id=1).values('category')
        response = HttpResponse(res[0]['category'])
        response['Access-Control-Allow-Origin'] = '*'
        return response

class GetSubcategory(View):
    def get(self, request):
        maitKey = request.GET.get('maitKey')
        res = Subcategory.objects.filter(maitKey=maitKey).values('subcategory')
        response = HttpResponse(res[0]['subcategory'])
        response['Access-Control-Allow-Origin'] = '*'
        return response

class GetSubcategoryDetail(View):
    def get(self, request):
        type = request.GET.get('type')
        miniWallkey = request.GET.get('miniWallkey')
        res = SubcategoryDetail.objects.filter(type=type, miniWallkey=miniWallkey).values('details')
        response = HttpResponse(res[0]['details'])
        response['Access-Control-Allow-Origin'] = '*'
        return response