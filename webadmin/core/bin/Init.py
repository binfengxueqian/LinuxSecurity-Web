from webadmin.core.lib.fileoperate import getDirData,collectFileData,listpool
from webadmin.core.lib.policy import setRule
from webadmin.core.lib.MD5 import getMD5
from webadmin.core.lib.log import *
from webadmin.core.lib.formatinfo import *
from webadmin.models import InitFile
from webadmin.models import Task_Log
from webadmin.models import Log_Msg
import time
import os

def main():
    print('开始')
    InitFile.objects.all().delete()
    now = time.time()
    tasktime = formatTime(now)
    # 任务日志开启
    tasklog = addTaskLogBegin(taskname='初始化数据库',tasktime= tasktime)
    addLogMsg('开始初始化数据库……',formatTime(time.time()))
    allfile = getDirData()
    groups = listpool(allfile,group=2000)
    logmsglist = []
    for group in groups:
        filegroup = []
        for filepath in group:
            initfile = InitFile()
            initfile.path = filepath.encode('UTF-8', 'ignore').decode('UTF-8')
            initfile.ruleType, initfile.ruleCheck = setRule(initfile.path)
            if not initfile.ruleCheck == '':
                try:
                    STAT = os.stat(initfile.path, follow_symlinks=False)
                    initfile.stat = str(STAT)
                    initfile.record = 'o'
                    initfile.MD5 = getMD5(initfile.path, initfile.ruleCheck, STAT.st_mode)
                    filegroup.append(initfile)
                except Exception as e:
                    addLogMsg(str(e), formatTime(time.time()))
                    logmsglist.append(Log_Msg(logmsg=str(e),taskid=tasklog.id))
        InitFile.objects.bulk_create(filegroup)
        print('完成' + str(groups.index(group)) + '/' + str(len(groups) - 1))
        addLogMsg('完成' + str(groups.index(group)) + '/' + str(len(groups) - 1), formatTime(time.time()))
    Log_Msg.objects.bulk_create(logmsglist)
    addTaskLogOver(tasklog,now)
    addLogMsg('数据库初始化完成\n总用时:'+str(tasklog.duration)+'\n共检查数据:'+str(len(allfile))+'个', 'over')

if __name__ == '__main__':
    # if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    #     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LinuxSecurity.settings')
    # # 第二种错误做如下设置，更新配置文件即可；
    # import django
    #
    # django.setup()
    # from webadmin.models import InitFile
    # from webadmin.models import Task_Log
    # from webadmin.models import Log_Msg


    main()
