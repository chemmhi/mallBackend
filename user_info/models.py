from django.db import models

# Create your models here.
class UserInfo(models.Model):
    nickName = models.CharField(max_length=20)
    phoneNumber = models.IntegerField(null=True)
    countBalance = models.IntegerField(null=True)
    coupon = models.IntegerField(null=True)
    coinPoint = models.IntegerField(null=True)
    message = models.CharField(max_length=100, null=True)