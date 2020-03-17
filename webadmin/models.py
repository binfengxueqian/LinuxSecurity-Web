from django.db import models

class UserInfo(models.Model):
    userid = models.IntegerField(primary_key=True,unique=True,verbose_name='用户ID',auto_created=True)
    username = models.CharField(max_length=20,unique=True,verbose_name='用户名',db_index=True,default='')
    password = models.CharField(max_length=64,verbose_name='密码')
    class Meta:
        verbose_name = '用户信息表'

class InitFile(models.Model):
    path = models.CharField(max_length=600,primary_key=True,verbose_name='文件路径')
    stat = models.CharField(max_length=200,default='',verbose_name='文件的属性')
    MD5 = models.CharField(max_length=32,default='',verbose_name='文件MD5值')
    ruleType = models.CharField(max_length=64,verbose_name='文件所属规则')
    ruleCheck = models.CharField(max_length=20,verbose_name='文件检查项')
    record = models.CharField(max_length=1,verbose_name='文件记录')
    class Meta:
        verbose_name = '文件属性表'

class InitFileBack(models.Model):
    path = models.CharField(max_length=600,primary_key=True,verbose_name='文件路径')
    stat = models.CharField(max_length=200,default='',verbose_name='文件的属性')
    MD5 = models.CharField(max_length=32,default='',verbose_name='文件MD5值')
    ruleType = models.CharField(max_length=64,verbose_name='文件所属规则')
    ruleCheck = models.CharField(max_length=20,verbose_name='文件检查项')
    record = models.CharField(max_length=1,verbose_name='文件记录')
    class Meta:
        verbose_name = '文件属性备份表'

class CheckFile(models.Model):
    id = models.IntegerField(verbose_name='ID',primary_key=True,auto_created=True)
    path = models.CharField(max_length=600,verbose_name='文件路径',db_index=True)
    stat = models.CharField(max_length=200,default='',verbose_name='文件的属性')
    MD5 = models.CharField(max_length=32,default='',verbose_name='文件MD5值')
    ruleType = models.CharField(max_length=64,verbose_name='文件所属规则')
    ruleCheck = models.CharField(max_length=20,verbose_name='文件检查项')
    record = models.CharField(max_length=1,verbose_name='文件记录')
    time = models.CharField(max_length=25,verbose_name='检查日期',default='',db_index=True)
    class Meta:
        verbose_name = '文件属性检查表'

class Task_Log(models.Model):
    id = models.IntegerField(verbose_name='ID', primary_key=True, auto_created=True)
    userid = models.IntegerField(verbose_name='用户ID')
    taskname = models.CharField(max_length=32,default='',verbose_name='任务名称')
    time = models.CharField(max_length=25,verbose_name='任务时间',default='',db_index=True)
    duration = models.IntegerField(default=0)
    state = models.CharField(max_length=1,verbose_name='任务状态',default='')
    class Meta:
        verbose_name = '任务日志表'

class Log_Msg(models.Model):
    id = models.IntegerField(verbose_name='ID', primary_key=True, auto_created=True)
    logmsg = models.CharField(max_length=32,default='',verbose_name='消息')
    taskid = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name = '日志消息表'

class SubDevice(models.Model):
    id = models.IntegerField(verbose_name='ID', primary_key=True, auto_created=True)
    deviceName = models.CharField(max_length=32,default='',verbose_name='设备名')
    deviceIP = models.CharField(max_length=15,default='',verbose_name='设备IP')
    deviceAddress = models.CharField(max_length=32,default='',verbose_name='设备所在地')
    class Meta:
        verbose_name = '子设备表'
# class PolGolVar(models.Model):
#     id = models.IntegerField(verbose_name='ID', primary_key=True, auto_created=True)
#     golbalvar = models.CharField(max_length=40,verbose_name='全局变量')
#     value = models.CharField(max_length=40,verbose_name='检查项')
#     class Meta:
#         verbose_name = '配置文件全局变量'

# class PolRule(models.Model):
#     id = models.IntegerField(verbose_name='ID', primary_key=True, auto_created=True)
#     rulename = models.CharField(max_length=64,verbose_name='规则名')
#     rulecheck = models.CharField(max_length=64,verbose_name='文件检查项')
#     severity = models.IntegerField(verbose_name='严重程度',default=60)
#     sec
#     class Meta:
#         verbose_name = '配置文件全局变量'