import os
import time
from Mail.ModelMail import ModelMail
from RSS.ModelBaiduTop import ModelBaiduTop
from RSS.ModelOsChina import ModelOsChina

q = {'8': 0, '11': 0, '14': 0, '17': 0, '20': 0}
# 三小时推送一次百度热搜
p = {'0': 0, '15': 0, '30': 0, '45': 0}
# 15分钟自动推送一次邮件
while True:
    ti = time.localtime(time.time())
    now_hour = ti.tm_hour
    now_minu = ti.tm_min
    if os.path.exists('pull_mail.txt'):
        os.remove('pull_mail.txt')
        mails = ModelMail(2)
        # 以上邮件手动推送部分
    if now_hour < 8 or now_hour > 20:
        # 休息时间，停下手头工作吧
        q['8'] = q['11'] = q['14'] = q['17'] = q['20'] = q['23'] = 0
        p['0'] = p['15'] = p['30'] = p['45'] = 0
    else:
        if now_hour >= 8 and now_hour < 11 and q['8'] == 0:
            q['8'] = 1
            baidu = ModelBaiduTop().push()
            oschina = ModelOsChina().push()
        elif now_hour >= 11 and now_hour < 14 and q['11'] == 0:
            q['11'] = 1
            baidu = ModelBaiduTop().push()
            oschina = ModelOsChina().push()
        elif now_hour >= 14 and now_hour < 17 and q['14'] == 0:
            q['14'] = 1
            baidu = ModelBaiduTop().push()
            oschina = ModelOsChina().push()
        elif now_hour >= 17 and now_hour < 20 and q['17'] == 0:
            q['17'] = 1
            baidu = ModelBaiduTop().push()
            oschina = ModelOsChina().push()
        elif now_hour >= 20 and q['20'] == 0:
            q['20'] = 1
            baidu = ModelBaiduTop().push()
            oschina = ModelOsChina().push()
        else:
            pass
        # 以上百度热搜推送部分
        if now_minu < 15 and p['0'] == 0:
            p['0'] = 1
            p['15'] = p['30'] = p['45'] = 0
            mails = ModelMail(1)
            oschina = ModelOsChina()
            baidu = ModelBaiduTop()
        elif now_minu >= 15 and now_minu < 30 and p['15'] == 0:
            p['15'] = 1
            p['0'] = p['30'] = p['45'] = 0
            mails = ModelMail(1)
            oschina = ModelOsChina()
            baidu = ModelBaiduTop()
        elif now_minu >= 30 and now_minu < 45 and p['30'] == 0:
            p['30'] = 1
            p['0'] = p['15'] = p['45'] = 0
            mails = ModelMail(1)
            oschina = ModelOsChina()
            baidu = ModelBaiduTop()
        elif now_minu >= 45 and p['45'] == 0:
            p['45'] = 1
            p['0'] = p['15'] = p['30'] = 0
            mails = ModelMail(1)
            oschina = ModelOsChina()
            baidu = ModelBaiduTop()
        else:
            pass
        # 以上邮件自动推送部分
    time.sleep(5)
