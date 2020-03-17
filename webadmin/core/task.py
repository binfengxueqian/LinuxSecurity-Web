import threading


class CallTask():


    def startInit(self):
        self.Threadlist = []
        for ts in threading.enumerate():
            self.Threadlist.append(ts.getName())
        from webadmin.core.bin import Init
        if 'initdatabaseThread' in self.Threadlist or 'checkfileThread' in self.Threadlist:
            return
        else:
            t = threading.Thread(target=Init.main, args=(), name='initdatabaseThread')
            t.start()
            return

    def startCheck(self):
        self.Threadlist = []
        for ts in threading.enumerate():
            self.Threadlist.append(ts.getName())
        from webadmin.core.bin import Check
        if 'initdatabaseThread' in self.Threadlist or 'checkfileThread' in self.Threadlist:
            return
        else:
            t = threading.Thread(target=Check.main, args=(), name='checkfileThread')
            t.start()
            return

    def executeSQL(self, SQLline,getdata=False,start=0,end=30):
        self.Threadlist = []
        for ts in threading.enumerate():
            self.Threadlist.append(ts.getName())
        result = {
            'code':200,
            'msg':''
        }
        if 'initdatabaseThread' in self.Threadlist or 'checkfileThread' in self.Threadlist:
            result['code']=1001
            result['msg'] = '正在执行其他操作，请稍后再试'
            return result
        else:
            try:
                result['data'] =[]
                from django.db import connection
                cursor = connection.cursor()
                cursor.execute(SQLline)
                try:
                    col_name_list = [tuple[0] for tuple in cursor.description]
                    rows = cursor.fetchall()
                    result['cols'] = col_name_list
                    result['rows'] = len(rows)
                    if getdata:
                        for i in rows[start:end]:
                            a = dict(zip(col_name_list,i))
                            result['data'].append(a)
                except Exception as e:
                    print(e)
                    result['code']=201
                    pass
                result['msg'] =SQLline+' 执行成功'
                cursor.close()
            except Exception as e:
                print(e)
                result['code'] = 1000
                result['msg'] = str(e)
        return result
