import os

# 项目目录
coreDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 配置文件存放目录
etcDir = os.path.join(coreDir,'etc')

# 配置文件路径
policyPath = os.path.join(etcDir, 'policy.txt')

# Report 的模板文件
reportModPath = os.path.join(etcDir,'report.mod')

# 定时检查配置文件
chectTimerPath = os.path.join(etcDir,'Timer.json')
# # Log文件夹地址
# logDir = os.path.join(coreDir,'log')
#
# # log文件地址
# logFilePath = os.path.join(logDir,'log.txt')