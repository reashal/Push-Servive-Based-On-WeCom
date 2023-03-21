from Mail import ReceiveMail
from WorkWX import ModelPush

'''
开发文档：python标准库
测试数据：QQ邮箱给163邮箱发件时获取的数据
'''

'''
由于163邮箱禁止非知名客户端以IMAP4协议登录
所以本项目采用POP3协议登录
'''

'''
更换账号/环境时可能需要更改的信息：
  Mail.ReceiveMail构造函数的参数
  Mail.ReceiveMail.connect_mail()中text = b'\r\n'.join(lines)
  Mail.ReceiveMail.get_mail_info()中第一个参数为企业微信用户id
'''


class ModelMail(object):
    def __init__(self, pull_type):
        # 此处传参(邮箱账号,邮箱客户端授权码,邮箱POP地址,POP端口)
        mails = ReceiveMail.ReceiveMail('账号@163.com', '客户端授权码', 'pop.163.com', 110)

        # 没有新未读邮件，自动执行时
        if mails.if_have_mail() == 0:
            # 手动推送才会提示没有新邮件
            if pull_type == 2:
                push = ModelPush.ModelPush(3)
                push.read_local()
                push.wx_push('企业微信员工账号', '', '', '', '', '', '邮箱账号')
            else:
                pass
        else:
            mails = mails.get_mail_info()
            push = ModelPush.ModelPush(1)
            push.read_local()
            # (用户,RSS内容/邮件内容,邮件标题,此刻时间,发件昵称,发件地址,收件地址)
            push.wx_push(mails[0], mails[1], mails[2], mails[3], mails[4], mails[5], mails[6])
            # print(mails)


if __name__ == '__main__':
    # mails = ReceiveMail.ReceiveMail('ruiyuqingshan@163.com', 'KHHOMQHVKCEKJGYZ', 'pop.163.com', 110)
    mails = ReceiveMail.ReceiveMail('777900@163.com', 'FEFOVGCWJMBYXCDX', 'pop.163.com', 110)
    if mails.if_have_mail() == 0:
        # 测试时看看有没有空邮件提醒
        push = ModelPush.ModelPush(3)
        push.read_local()
        push.wx_push('企业微信员工账号', '', '', '', '', '', '邮箱账号')
    else:
        mails = mails.get_mail_info()
        push = ModelPush.ModelPush(1)
        push.read_local()
        push.wx_push(mails[0], mails[1], mails[2], mails[3], mails[4], mails[5], mails[6])
        # print(mails)
