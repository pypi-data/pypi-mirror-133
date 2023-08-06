import time
import datetime


"""
指定时间：年月日时分秒运行程序
"""
def timed(function,*times,data=None):
    _EXEtime_=datetime.datetime(*times)
    if str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))==str(_EXEtime_):
        if data == None:
            function()
        else:
            function(data)
    else:
        pass
    time.sleep(1)

"""
指定时间：时运行程序
"""
def timed_hour(function,hour=0,data=None):
    if str(datetime.datetime.now().strftime("%H"))==str(hour):
        if data == None:
            function()
        else:
            function(data)
    else:
        pass
    time.sleep(1)
"""
指定时间：分钟运行程序
"""
def timed_minute(function,minute=0,data=None):
    if str(datetime.datetime.now().strftime("%M"))==str(minute):
        if data == None:
            function()
        else:
            function(data)
    else:
        pass
    time.sleep(1)
