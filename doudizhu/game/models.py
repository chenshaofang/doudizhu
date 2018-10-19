from django.db import models
from index.models import *
# Create your models here.
class Game(models.Model):
    room_id = models.ForeignKey(Room,null=True)
    user_id = models.OneToOneField(UserInfo,null=True)
    serial_number = models.IntegerField('序号',null=False,default=0)
    brand = models.CharField('牌',max_length=500,null=True)
    def __str__(self):
        return self.brand