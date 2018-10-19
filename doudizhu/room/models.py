from django.db import models

class Room(models.Model):
    room_name = models.CharField('房间名',max_length=10,null=False)
    room_root = models.CharField('房主',max_length=10,null=False)
    state = models.BooleanField('状态',default=True)
    number = models.IntegerField('人数',default=0,null=True)
