from django.db import models
from room.models import *
# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField('昵称',max_length=10,null=False)
    uimg = models.ImageField('头像',upload_to='touxiang',null=True)
    uphone = models.CharField('手机号',max_length=20,null=False)
    upwd = models.CharField('密码',max_length=20,null=False)
    ucoin = models.IntegerField('金币',null=True,default=5000)
    room_n = models.ForeignKey(Room,null=True)
    isActiv = models.BooleanField('激活',default=True)

