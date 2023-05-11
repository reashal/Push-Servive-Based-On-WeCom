from Mail import ReceiveMail
from WorkWX import ModulePush

# 邮件模块已封装好，主函数直接调用本构造函数即可，只需注意传参，修改点看注释

'''
更换账号/环境时可能需要更改的信息：
  Mail.ReceiveMail构造函数的参数
  Mail.ReceiveMail.get_mail_info()中第一个参数为企业微信用户id
'''


class ModuleMail(object):
    def __init__(self, pull_type):
        # 形参为1代表系统定时执行的，没有未读邮件也不再提醒；形参为2代表用户主动发起的请求，没有未读邮件也提醒。
        # 需要添加多个邮箱，自己按需修改
        mails = ReceiveMail.ReceiveMail('****@163.com', 'A******', 'pop.163.com', 110)
        # 此处传参[邮箱账号,邮箱客户端授权码(并非邮箱密码),邮箱POP地址,POP端口]
        if mails.if_have_mail() == 0:
            # 如果此账号没有未读邮件
            if pull_type == 2:
                # 用户主动发起的请求才会提示没有新邮件
                push = ModulePush.ModulePush(3)
                # 参数如果是1代表系统定时拉取邮件
                # 参数如果是2代表RSS的普通文本消息
                # 参数如果是3代表用户拉取邮件
                push.read_local()
                push.wx_push('******', '', '', '', '', '', '******@163.com')
                # 参数 [企业微信用户, 消息内容(邮件正文/订阅消息), 邮件主题, 邮件发送时间, 发件人昵称, 发件人邮箱, 收件人地址]
                # 只写了一个邮箱，其它按需修改
            else:
                pass
        else:
            # 如果此账号有未读邮件
            mails = mails.get_mail_info()
            push = ModulePush.ModulePush(1)
            push.read_local()
            # [用户,RSS内容/邮件内容,邮件标题,邮件发送时间,发件人昵称,发件人地址,收件人地址]
            push.wx_push(mails[0], mails[1], mails[2], mails[3], mails[4], mails[5], mails[6])


if __name__ == '__main__':
    mails = ReceiveMail.ReceiveMail('****@163.com', 'A******', 'pop.163.com', 110)
    if mails.if_have_mail() == 0:
        push = ModulePush.ModulePush(3)
        push.read_local()
        push.wx_push('******', '', '', '', '', '', '******@163.com')
    else:
        mails = mails.get_mail_info()
        push = ModulePush.ModulePush(1)
        push.read_local()
        push.wx_push(mails[0], mails[1], mails[2], mails[3], mails[4], mails[5], mails[6])
