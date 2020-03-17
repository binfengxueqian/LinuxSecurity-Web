import psutil
import time
def getmemory():
    mem = psutil.virtual_memory()
    memory = {}
    memory['free'] = mem.free
    memory['total'] = mem.total
    memory['cached'] = mem.cached
    memory['buffers'] = mem.buffers
    memory['available'] = mem.available
    memory['percent'] = mem.percent
    memory['used'] = mem.used
    return memory

def getcpu():
    cpu = {
        'percent':psutil.cpu_percent(percpu=True),
        'logicalcount':psutil.cpu_count(),
        'time':time.strftime("%H:%M:%S", time.localtime(time.time())),
        'count':psutil.cpu_count(logical=False)
    }
    return cpu
def getdisk():
    disks = []
    root = psutil.disk_usage('/')
    home = psutil.disk_usage('/home')
    rootd = {
        'used':root.used,
        'free':root.free,
        'total':root.total,
        'percent':root.percent
    }
    homed = {
        'used': home.used,
        'free': home.free,
        'total': home.total,
        'percent': home.percent
    }
    disks.append(rootd)
    disks.append(homed)
    return disks