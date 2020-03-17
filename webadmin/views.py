from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from webadmin.models import UserInfo,InitFile,CheckFile,Task_Log,SubDevice
from django.contrib.auth.hashers import make_password ,check_password
from webadmin.auth.token import create_token
from webadmin.core.bin import Check
from django.db import transaction
import re,json
from webadmin.core.lib.systeminfo import getmemory,getcpu,getdisk
from webadmin.core.lib.log import logmsg
from apscheduler.schedulers.background import BackgroundScheduler
from webadmin.core.lib.config import chectTimerPath

class login(View):
    def get(self,request):
        return render(request,'login.html')
    def post(self,request):
        result = {}
        info = request.POST.dict()
        try:
            userinfo = UserInfo.objects.get(username=info['username'])
            if(check_password(info['password'],userinfo.password)):
                result['code']=200
                result['msg'] = '登录成功'
                payload = {
                    'username':info['username']
                }
                exp = 60*60*24
                token = create_token(payload,exp)
                result['token']=str(token,encoding='utf8')
                result['token_age']=exp
                return JsonResponse(result)
            else:
                result['code']=1002
                result['msg'] = '密码错误'
        except:
            result['code']=1001
            result['msg']='没有此用户'
        return JsonResponse(result)

def index(request):
    return render(request, 'index.html')

def checkPassword(request):
    password = request.POST.get('password')
    username = request.user
    result = {}
    try:
        user = UserInfo.objects.get(username=username)
        if(check_password(password,user.password)):
            result['code']=200
            result['msg'] = '密码正确'
        else:
            result['code'] = 1001
            result['msg'] = '输入密码错误'
        return JsonResponse(result)
    except:
        return render(request, 'login.html')

class admin_changepass(View):
    def get(self,request):
        return render(request, 'admin_changepass.html')
    def post(self,request):
        password = request.POST.get('password')
        oldPassword = request.POST.get('oldPassword')
        username = request.user
        result = {}
        try:
            user = UserInfo.objects.get(username=username)
            if check_password(oldPassword,user.password):
                user.password = make_password(password)
                user.save()
                result['code'] = 200
                result['msg'] = '修改密码成功'
            else:
                result['code'] = 1002
                result['msg'] = '原始密码错误'
        except:
            result['code'] = 1001
            result['msg'] = '修改密码失败'
        return JsonResponse(result)

class task_msg(View):
    def get(self, request):
        from webadmin.core.task import CallTask
        params = request.GET.dict()
        try:
            if params['action']=='initdatabase':
                CallTask().startInit()
            if params['action']=='checkfile':
                CallTask().startCheck()
            return render(request, 'task_msg.html')
        except Exception as e:
            print(e)
            return HttpResponse("你所访问的页面不存在",status=404)

    def post(self, request):
        global logmsg
        result = {}
        result['code'] = 200
        if not logmsg==[]:
            result['data'] = []
            result['data'].extend(logmsg)
            logmsg.clear()
        else:
            result['code'] = 1000
            result['msg'] = '…'
        return JsonResponse(result)

class checkdbshow(View):
    def get(self,request):
        params = request.GET.dict()
        if not 'page' in params:
            query = re.sub("'(\w+)':","\\1:",str(params))
            return render(request, 'checkDB.html',context={'query':query})
        else :
            page = int(params['page'])
            limit = int(params['limit'])

            result = {}
            result['code'] = 0
            if 'time'in params:
                time = params['time']
                result['count'] = CheckFile.objects.filter(time=time).count()
                rows = CheckFile.objects.filter(time=time)[(page - 1) * limit:page * limit]
            else:
                result['count'] = CheckFile.objects.all().count()
                rows = CheckFile.objects.all()[(page - 1) * limit:page * limit]
            result['msg'] = '查询成功'
            result['data'] = []
            for row in rows:
                datadict = row.__dict__
                datadict.pop('_state')
                result['data'].append(datadict)
            return JsonResponse(result)

    def post(self,request):
        params = request.POST.dict()
        result = {}
        result['code'] = 200
        if 'del' in params:
            ids = params['del'].split(',')[:-1]
            print(ids)
            try:
                with transaction.atomic():
                    for id in ids:
                        CheckFile.objects.get(id=int(id)).delete()
                result['msg'] = '删除成功'
                return JsonResponse(result)
            except Exception as e:
                result['msg'] = str(e)
                return JsonResponse(result)
        if 'update' in params:
            ids = params['update'].split(',')[:-1]
            try:
                with transaction.atomic():
                    for id in ids:
                        file = CheckFile.objects.get(id=int(id))
                        print(file.path)
                        try:
                            initfile = InitFile.objects.get(path=file.path)
                            initfile.stat = file.stat
                            initfile.MD5 = file.MD5
                            initfile.save()
                        except:
                            InitFile.objects.create(path=file.path,
                                                stat=file.stat,
                                                MD5=file.MD5,
                                                ruleCheck=file.ruleCheck,
                                                ruleType=file.ruleType,
                                                record=file.record)
                        file.delete()
                result['msg'] = '更新成功'
                return JsonResponse(result)
            except Exception as e:
                print(e)
                result['msg'] = str(e)
                return JsonResponse(result)

class initdbshow(View):
    def get(self,request):
        params = request.GET.dict()
        if params=={}:
            return render(request, 'initDB.html')
        else:
            page = int(params['page'])
            limit = int(params['limit'])
            result = {}
            result['code'] = 0
            result['count'] = InitFile.objects.all().count()
            rows = InitFile.objects.all()[(page - 1) * limit:page * limit]
            result['msg'] = '查询成功'
            result['data'] = []
            for row in rows:
                datadict = row.__dict__
                datadict.pop('_state')
                result['data'].append(datadict)
            return JsonResponse(result)

def log(request):
    params = request.GET.dict()
    result = {}
    result['code'] = 200
    try:
        if params == {}:
            return render(request,'log.html')
        else:
            if params['action'] == 'getlog':
                result['data'] = []
                rows = Task_Log.objects.all()
                for row in rows:
                    log = {}
                    log['time'] = row.time
                    log['user'] = UserInfo.objects.get(userid=row.userid).username
                    log['taskname'] = row.taskname
                    log['duration'] = row.duration
                    if row.state=='s':
                        log['state'] = '成功'
                    else:
                        log['state'] = '失败'
                    result['data'].append(log)
                result['data'].reverse()
                return JsonResponse(result)
    except Exception as e:
        result['code'] = 1000
        result['msg'] = str(e)
        return JsonResponse(result)

def home(request):
    params = request.GET.dict()
    result = {}
    result['code'] = 200
    if 'action'in params:
        if params['action'] == 'gethtml':
            return render(request,'./home.html')
        elif params['action']=='getsysteminfo':
            result['memory'] = getmemory()
            result['disks'] = getdisk()
            result['cpu'] = getcpu()
            return JsonResponse(result)
    else:
        return render(request,'error.html')

class Timer(View):
    scheduler = BackgroundScheduler()
    def get(self,request):
        params = request.GET.dict()
        if 'action' in params:
            if params['action']=='getconf':
                result = {
                    'code':200,
                    'data':[],
                    'msg':''
                }
                try:
                    f = open(chectTimerPath,'r',encoding='utf-8')
                    result['data'] = json.load(f)
                    result['msg'] = '配置文件加载成功'
                except Exception as e:
                    result['code']=1000
                    result['msg']=str(e)
                return JsonResponse(result)
            else:
                pass
        else:
            pass
        return render(request,'Timer.html')
    def post(self,request):
        from webadmin.core.task import CallTask
        result={
            'code':200,
            'msg':''
        }
        params = request.POST.dict()
        if 'action' in params:
            if params['action']=='updataConf':
                params.pop('action')
                with open(chectTimerPath,'w',encoding='utf-8')as f:
                    json.dump(params,f,indent=4)
                try:
                    timerConf = params
                    if self.scheduler.get_job('TimerCheck'):
                        self.scheduler.remove_job('TimerCheck')
                    if (timerConf['enable']):
                        if (timerConf['tigger'] == 'appoint'):
                            week = timerConf['week'][:-1].replace('.', ',')
                            time = timerConf['selecttime'].split(':')
                            self.scheduler.add_job(CallTask().startCheck, 'cron',
                                                   day_of_week=week,
                                                   hour=int(time[0]),
                                                   minute=int(time[1]),
                                                   second=int(time[2]),
                                                   id='TimerCheck')
                        else:
                            interval = timerConf['intervaltime'].split(':')
                            self.scheduler.add_job(CallTask().startCheck, 'interval',
                                                   days=int(interval[0]),
                                                   hours=int(interval[1]),
                                                   minutes=int(interval[2]),
                                                   seconds=int(interval[3]),
                                                   id='TimerCheck')
                    result['msg'] = '配置更新成功'
                except:
                    result['code']=1003
                    result['msg'] = '配置更新失败'
            elif params['action']=='startTask':
                if self.scheduler.get_job('TimerCheck'):
                    self.scheduler.start()
                    result['msg'] = '定时任务启动成功'
                else:
                    result['code'] = 1004
                    result['msg'] = '请先启用定时任务'
            elif params['action']=='stopTask':
                if self.scheduler.get_job('TimerCheck'):
                    self.scheduler.remove_job('TimerCheck')
                    result['msg'] = '定时任务停止成功'
                else:
                    result['code'] = 1005
                    result['msg'] = '未启用定时任务'
            else:
                result['code'] = 1001
                result['msg'] = '未指明action'
        else:
            result['code']=1000
            result['msg']='传入参数错误，缺少"action"参数'
        return JsonResponse(result)

class developer(View):
    def get(self,request):
        return render(request,'developer.html')
    def post(self,request):
        result = {
            'code':200,
            'msg':''
        }
        params = request.POST.dict()
        try:
            if params['action']=='executeSQL':
                result['msg'] = '请求已收到'
                from webadmin.core.task import CallTask
                res = CallTask().executeSQL(params['SQLline'])
                if res['code']==200:
                    result['msg'] = res['msg']
                    result['rows'] = res['rows']
                    result['cols'] = res['cols']
                else:
                    result['code'] = res['code']
                    result['msg'] = res['msg']

            if params['action']=='getData':
                page = int(params['page'])
                limit = int(params['limit'])
                from webadmin.core.task import CallTask
                res = CallTask().executeSQL(params['SQLline'],True,(page - 1) * limit,page * limit)
                result = {}
                result['code'] = 0
                result['count'] = res['rows']
                result['msg'] = '查询成功'
                result['data'] = res['data']
        except:
            result['code'] = 1000
            result['msg'] = '请求参数错误'
        return JsonResponse(result)

class bindSubDevice(View):
    def get(self,request):
        return render(request,'BindSubdevice.html')
    def post(self,request):
        result = {
            'code':200,
            'msg':'请求以收到'
        }
        params = request.POST.dict()

        return JsonResponse(result)
