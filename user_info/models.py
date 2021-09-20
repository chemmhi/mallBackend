from django.db import models

# Create your models here.
class UserInfo(models.Model):
    userName = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    phoneNumber = models.IntegerField()
    countBalance = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    coinPoint = models.IntegerField(null=True)
    message = models.CharField(max_length=100, null=True)
    cart = models.JSONField(null=True)
    sessionId = models.CharField(max_length=100,null=True)