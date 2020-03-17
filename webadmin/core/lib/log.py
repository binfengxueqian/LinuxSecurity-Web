
from webadmin.models import Task_Log
from webadmin.models import Log_Msg
logmsg = []
import time
def addLogMsg(msg,strtime):
    global logmsg
    log = {}
    log['msg'] = msg
    log['time'] = strtime
    logmsg.append(log)
    # if strtime=='over':
    #     time.sleep(2)
    #     logmsg = []


def addTaskLogBegin(taskname,tasktime,userid = 1):
    tasklog = Task_Log(taskname=taskname, time=tasktime, state='f', userid=userid, duration=0)
    tasklog.save()
    tasklog = Task_Log.objects.get(time=tasktime, state='f')
    return tasklog
def addTaskLogOver(tasklog,now):
    tasklog.duration = (int(time.time()-now))
    tasklog.state = 's'
    tasklog.save()