import os
import time
from Mail.ModuleMail import ModuleMail
from RSS.ModuleBaiduTop import ModuleBaiduTop
from RSS.ModuleOsChina import ModuleOsChina

'''
    1.形如 Module*** 为各模块封装完毕的成品，只需在此调用成品即可
    2.邮件模块仅需 new ModuleMail( * ) 参数需要注意
    3.订阅模块以百度热搜为例，先 new ModuleBaiduTop()解析热搜内容并更新到前端界面，如果需要推送再执行 .push()
'''

q = {'8': 0, '11': 0, '14': 0, '17': 0, '20': 0}
# 三小时推送一次百度热搜
p = {'0': 0, '15': 0, '30': 0, '45': 0, '5': 0}
# 15分钟自动推送一次邮件
while True:
    ti = time.localtime(time.time())
    now_hour = ti.tm_hour
    now_minu = ti.tm_min
    if os.path.exists('pull_mail.txt'):
        os.remove('pull_mail.txt')
        mails = ModuleMail(2)
        # 每隔五秒检测用户是否提交邮件拉取请求，没有则提示
    if now_hour % 10 == 0:
        if p['5'] == 0:
            baidu = ModuleBaiduTop()
            oschina = ModuleOsChina()
            p['5'] = 1
    else:
        p['5'] = 0
        # 每隔五分钟更新订阅信息
    if now_hour < 8 or now_hour > 20:
        # 休息时间，停下手头工作吧。定时任务不再执行，手动任务不受影响
        q['8'] = q['11'] = q['14'] = q['17'] = q['20'] = q['23'] = 0
        p['0'] = p['15'] = p['30'] = p['45'] = 0
    else:
        # 每隔三小时群体推送一次订阅信息
        if now_hour >= 8 and now_hour < 11 and q['8'] == 0:
            q['8'] = 1
            baidu = ModuleBaiduTop().push()
            oschina = ModuleOsChina().push()
        elif now_hour >= 11 and now_hour < 14 and q['11'] == 0:
            q['11'] = 1
            baidu = ModuleBaiduTop().push()
            oschina = ModuleOsChina().push()
        elif now_hour >= 14 and now_hour < 17 and q['14'] == 0:
            q['14'] = 1
            baidu = ModuleBaiduTop().push()
            oschina = ModuleOsChina().push()
        elif now_hour >= 17 and now_hour < 20 and q['17'] == 0:
            q['17'] = 1
            baidu = ModuleBaiduTop().push()
            oschina = ModuleOsChina().push()
        elif now_hour >= 20 and q['20'] == 0:
            q['20'] = 1
            baidu = ModuleBaiduTop().push()
            oschina = ModuleOsChina().push()
        else:
            pass
        # 每隔十五分钟查看是否有未读邮件，没有则不提醒
        if now_minu < 15 and p['0'] == 0:
            p['0'] = 1
            p['15'] = p['30'] = p['45'] = 0
            mails = ModuleMail(1)
        elif now_minu >= 15 and now_minu < 30 and p['15'] == 0:
            p['15'] = 1
            p['0'] = p['30'] = p['45'] = 0
            mails = ModuleMail(1)
        elif now_minu >= 30 and now_minu < 45 and p['30'] == 0:
            p['30'] = 1
            p['0'] = p['15'] = p['45'] = 0
            mails = ModuleMail(1)
        elif now_minu >= 45 and p['45'] == 0:
            p['45'] = 1
            p['0'] = p['15'] = p['30'] = 0
            mails = ModuleMail(1)
        else:
            pass
    time.sleep(5)
