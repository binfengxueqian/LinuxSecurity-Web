from webadmin.core.lib.policy import setRule
from webadmin.core.lib.fileoperate import *
from webadmin.core.lib.mystat import *
from webadmin.core.bin.PrintReport import pReport
import time
from django.db import transaction
from webadmin.models import CheckFile
from webadmin.models import InitFileBack
from webadmin.core.lib.log import addLogMsg, addTaskLogBegin, addTaskLogOver

dbcolumn = None
cursor = None

def createRemoveFile(date):
    a = time.time()
    # cursor.execute("delete from webadmin_initfileback where record = 'c'")
    cursor.execute("select * from webadmin_initfileback where record = 'o'")
    result = cursor.fetchall()
    filesindb = []
    print(len(result))
    for row in result:
        fileindb = dict(zip(dbcolumn, row))
        fileindb['record'] = 'r'
        fileindb['time'] = date
        filesindb.append(CheckFile(
            path=fileindb['path'],
            stat=fileindb['stat'],
            MD5=fileindb['MD5'],
            ruleCheck=fileindb['ruleCheck'],
            ruleType=fileindb['ruleType'],
            record=fileindb['record'],
            time=fileindb['time']))
    CheckFile.objects.bulk_create(filesindb)
    print(time.time() - a)

@transaction.atomic()
def checkChange(allfile,date):
    groups = listpool(allfile, group=5000)
    for group in groups:
        checkfilegroup = []
        for filepath in group:
            a = time.time()
            checkfile = CheckFile()
            checkfile.time = date
            checkfile.path = filepath.encode('UTF-8', 'ignore').decode('UTF-8')
            checkfile.ruleType, checkfile.ruleCheck = setRule(checkfile.path)
            if not checkfile.ruleCheck == '':
                try:
                    # fileindbobj = InitFileBack.objects.get(path=checkfile.path)
                    # fileindb = fileindbobj.__dict__
                    # fileindbobj.delete()
                    cursor.execute("select * from webadmin_initfileback where path = '%s'" % checkfile.path)
                    row = cursor.fetchall()[0]
                    fileindb = dict(zip(dbcolumn, row))
                    cursor.execute("delete from webadmin_initfileback where path = '%s'" % checkfile.path)
                    try:
                        STAT = os.stat(checkfile.path, follow_symlinks=False)
                        checkfile.stat = str(STAT)
                        originStat = Mystat(fileindb['stat']).__dict__  # 获取原始的stat
                        newStat = Mystat(checkfile.stat).__dict__  # 刚获取的stat
                        for i in checkfile.ruleCheck:
                            if i in StatMap:
                                if originStat[StatMap[i]] != newStat[StatMap[i]]:
                                    # addLogMsg('被修改的文件' + checkfile.path, formatTime(time.time()))
                                    checkfile.record = 'm'
                                    checkfilegroup.append(checkfile)
                                    checkfile.MD5 = getMD5(checkfile.path, checkfile.ruleCheck, STAT.st_mode)
                                    break
                            if i in 'CMHS':
                                checkfile.MD5 = getMD5(checkfile.path, checkfile.ruleCheck, STAT.st_mode)
                                if fileindb['MD5'] != checkfile.MD5:
                                    # addLogMsg('MD5被修改的文件' + checkfile.path, formatTime(time.time()))
                                    checkfile.record = 'm'
                                    checkfilegroup.append(checkfile)
                                    break
                    except Exception as e:
                        addLogMsg(str(e), formatTime(time.time()))
                # 新增文件
                except:
                    try:
                        STAT = os.stat(checkfile.path, follow_symlinks=False)
                        checkfile.record = 'a'
                        checkfile.stat = STAT
                        checkfile.MD5 = getMD5(checkfile.path, checkfile.ruleCheck, STAT.st_mode)
                        # addLogMsg('新增文件：' + checkfile.path, formatTime(time.time()))
                        checkfilegroup.append(checkfile)
                    except Exception as e:
                        addLogMsg(str(e), formatTime(time.time()))
            # print(time.time() - a)

        CheckFile.objects.bulk_create(checkfilegroup)
        print('完成'+str(groups.index(group))+'/'+str(len(groups)-1))
        addLogMsg('完成'+str(groups.index(group))+'/'+str(len(groups)-1), formatTime(time.time()))

def main():
    from django.db import connection
    global cursor
    global dbcolumn
    cursor = connection.cursor()
    dbcolumn = re.search('\((.*?)\)', InitFileBack.__doc__).group(1).split(', ')
    # InitFileBack.objects.all().delete()
    cursor.execute('delete from webadmin_initfileback')
    now = time.time()
    # 数据表复制
    addLogMsg('开始Check', formatTime(now))
    # print('开始check')

    cursor.execute('insert into webadmin_initfileback select * from webadmin_initfile')
    tasklog = addTaskLogBegin(taskname='文件完整性检查',tasktime=formatTime(now))
    allfile = getDirData()
    addLogMsg('文件扫描完成', formatTime(time.time()))
    checkChange(allfile,formatTime(now))
    createRemoveFile(formatTime(now))
    addTaskLogOver(tasklog,now)
    # cursor.execute("vacuum")
    # print('结束')
    # print(time.time()-now)
    # print(InitFileBack.objects.all().count())
    addLogMsg('Check完成', formatTime(time.time()))
    addLogMsg('改动文件总数：'+str(CheckFile.objects.filter(time=formatTime(now)).count()), formatTime(time.time()))
    addLogMsg('用时：'+str(time.time()-now), 'over')
    cursor.close()
    # pReport(checkDBPath,checkTxtPath)
if __name__ == '__main__':
    # if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    #     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LinuxSecurity.settings')
    # # 第二种错误做如下设置，更新配置文件即可；
    # import django
    #
    # django.setup()
    # from webadmin.models import InitFile
    # from webadmin.models import CheckFile
    # from webadmin.models import InitFileBack
    # from django.db import connection
    # from webadmin.core.lib.log import addLogMsg, addTaskLogBegin, addTaskLogOver
    # cursor = connection.cursor()
    # dbcolumn = re.search('\((.*?)\)', InitFileBack.__doc__).group(1).split(', ')
    main()


