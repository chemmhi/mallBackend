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