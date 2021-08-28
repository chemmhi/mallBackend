from django.db import models

# Create your models here.
class HomeMultidata(models.Model):
    home_multidata = models.JSONField()

class HomeGoods(models.Model):
    content = models.JSONField()
    type = models.CharField(max_length=10)
    page = models.IntegerField()


class Details(models.Model):
    iid = models.CharField(max_length=15)
    goods = models.JSONField()


class Redommend(models.Model):
    recommend = models.JSONField()


class Category(models.Model):
    category = models.JSONField()

class Subcategory(models.Model):
    subcategory = models.JSONField()
    maitKey = models.CharField(max_length=15)

class SubcategoryDetail(models.Model):
    miniWallkey = models.CharField(max_length=20)
    type = models.CharField(max_length=15)
    details = models.JSONField()