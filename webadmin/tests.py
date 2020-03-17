from django.test import TestCase
import time
import os
# import threading
import re
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LinuxSecurity.settings')

# 第二种错误做如下设置，更新配置文件即可；
import django
django.setup()

# from webadmin.models import InitFile
from webadmin.models import CheckFile
# from webadmin.models import InitFileBack
# from webadmin.models import Task_Log
from django.contrib.auth.hashers import make_password
# from django.db import transaction
# from webadmin.core.bin import Check
from django.db import connection
# from webadmin.models import UserInfo
# a = UserInfo(username='admin',password=make_password('admin'))
# a.save()
# cursor = connection.cursor()
# cursor.execute('delete from webadmin_checkfile')

# cursor.execute('delete from webadmin_task_log')
# cursor.close()
# cursor.execute('select count(id) from webadmin_checkfile')
# # cursor.execute('select count(id) from webadmin_checkfile')
# # cursor.execute('select count(id) from webadmin_task_log')
# result = cursor.fetchall()
# for i in result:
#     print(i)
# from multiprocessing import Process
# t = threading.Thread(target=Check.main,args=())
# t.start()
# CheckFile.objects.all().delete()
# InitFileBack.objects.all().delete()
# InitFile.objects.all().delete()
# print(Task_Log.objects.all().count())

# file = CheckFile.objects.get(id=23)
# print(file)
# file.delete()
CheckFile.objects.all().delete()
# cursor = connection.cursor()
# checkfilet.join()
# Check.main()
# print(CheckFile.objects.all().count())
# print(InitFile.objects.all().count())
# print(InitFileBack.objects.all().count())
# print(CheckFile.objects.all().count())
# InitFileBack.objects.all().delete()
# CheckFile.objects.all().delete()

# tasklog = Task_Log(taskname='初始化数据库',time='2020年03月05日03:05:39',state='f',userid = 1,duration=0)
# print(tasklog.save())
# tasklog = Task_Log.objects.get(time='2020年03月05日03:05:39',state='s')
# Task_Log.objects.all().delete()
# print(tasklog.id)
# now = time.time()
# InitFileBack.objects.bulk_create(InitFile.objects.all())
# print(time.time()-now)
# print(InitFileBack.objects.all().count())

# Create your tests here.
#
# cursor = connection.cursor()
# cursor.execute("update webadmin_initfileback set record = 'c' where path = '%s'",('/'))

# cursor.execute("select * from webadmin_checkfile where record='r'")
# for row in cursor.fetchall():
#     print(row)
#
# # transaction.commit_unless_managed()
# cursor.close()

