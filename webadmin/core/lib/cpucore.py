import psutil
# cpu时间
print('CPU时间',psutil.cpu_times())

# CPU逻辑核心
print('CPU逻辑核心',psutil.cpu_count())
# CPU物理核心
print('CPU物理核心',psutil.cpu_count(logical=False))
# CPU使用率
print(psutil.cpu_percent(percpu=True))

# 系统内存
mem = psutil.virtual_memory()
print('系统内存信息',mem)
# 系统总内存
print('系统总内存',mem.total/1024/1024)
# 系统可用内存
print('系统可用内存',mem.available/1024/1024)
# 系统总内存
print('系统已用',mem.used/1024/1024)
# 系统剩余内存
print('系统剩余内存',mem.free/1024/1024)
# 系统buffer
print('系统buffer',mem.buffers/1024/1024)
# 系统cached
print('系统cached',mem.cached/1024/1024)
# 系统内存使用率
print('系统内存使用率',mem.percent,'%')


# 系统进程
print(psutil.pids().__len__())
# for i in psutil.pids():
#     print(psutil.Process(i))
p = psutil.Process(1)
print('进程名',p.name())            #进程名
print('进程的bin路径',p.exe())            #进程的bin路径
print('进程的工作目录绝对路径',p.cwd())            #进程的工作目录绝对路径
print('进程状态',p.status())            #进程状态
print('进程创建时间',p.create_time())            #进程创建时间
print('进程uid信息',p.uids())            #进程uid信息
print('进程的gid信息',p.gids())            #进程的gid信息
print('进程的cpu时间信息',p.cpu_times())            #进程的cpu时间信息,包括user,system两个cpu信息
print('进程cpu亲和度',p.cpu_affinity())            #get进程cpu亲和度,如果要设置cpu亲和度,将cpu号作为参考就好
print('进程内存利用率',p.memory_percent())            #进程内存利用率
print('进程内存rss,vms信息',p.memory_info())            #进程内存rss,vms信息
print('进程的IO信息',p.io_counters())            #进程的IO信息,包括读写IO数字及参数
# print('返回进程列表',p.connectios())            #返回进程列表
print('进程开启的线程数',p.num_threads())            #进程开启的线程数

# 系统用户
# print(psutil.users())
for user in psutil.users():
    print(user)

print('-----------------------------磁盘信息---------------------------------------')
io = psutil.disk_partitions()
print("系统磁盘信息：" + str(io))
for i in io:
    print(i)
print(psutil.disk_usage('/').total/1024/1024/1024) # 磁盘使用情况
print(psutil.disk_usage('/').__dict__)
# print(mem.__dict__)