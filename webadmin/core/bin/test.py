import sqlite3
from webadmin.core.lib.config import *
connect = sqlite3.connect(initDB_Path)
c = connect.cursor()
# c.execute("select * from main.FILEDB where path='/'")
c.execute("select count(PATH) from main.FILEDB where MD5!=''")
# c.execute("select * from main.FILEDB where MD5!='' limit 6")
results = c.fetchall()
for row in results:
    print(row)
c.close()
connect.close()