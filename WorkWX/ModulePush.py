from WorkWX.GetToken import *
from WorkWX.SendMessage import *

'''
已封装好的企业微信推送模块实现流程：
    1.第一次先获取token（本地优先，无效再从缓存读）
    2.验证token后，短时间内连续推送内容
调用说明：
    1.new 构造函数()，注意参数
    2.read_local()读取本地token
    3.wx_push()推送消息
仅需注意两处改动：
    1.构造函数参数代表推送的消息类型
    2.更换企业微信应用配置项需要改动构造函数
'''


# 后期可能需要改这里

class ModulePush:
    def __init__(self, msg_type):
        # 参数如果是1代表系统定时拉取邮件
        # 参数如果是2代表RSS的普通文本消息
        # 参数如果是3代表用户拉取邮件
        self.CORP_ID = "企业ID"  # 我的企业 企业ID
        self.SECRET = "自建应用SECRET"  # 自建应用SECRET
        self.AGENT_ID = "自建应用AgentID"  # 自建应用AgentId
        self.token = "0"
        self.msg_type = msg_type

    def read_local(self):
        # token接口不能频繁调用，否则会被拦截，此处选用本地缓存
        # 先从缓存里获取,没有或失效再重新用接口获取
        # 发连续消息之前本函数仅需调用一次
        try:
            f = open("token.txt", 'r')
        except  FileNotFoundError as e:
            # 如果是第一次执行程序，没有缓存会抛出文件不存在的异常
            # 处理方式：创建文件，从接口获取token并将之写入文件
            f = open("token.txt", "w")
            self.token = GetToken(self.CORP_ID, self.SECRET, self.AGENT_ID).token
            f.write(self.token)
        else:
            self.token = f.read()
            print("本次token为缓存获取")
        finally:
            f.close()

    def wx_push(self, usr, content, sub, ti, from_name, from_add, to_add):
        # [用户,RSS内容/邮件内容,邮件标题,邮件发送时间,发件人昵称,发件人地址,收件人地址]
        if self.msg_type == 1:
            # 系统定时执行的邮件模块
            send_msg = SendMessage(self.token, self.AGENT_ID, self.msg_type, usr, content, sub, ti,
                                   from_name, from_add, to_add)
        elif self.msg_type == 2:
            # 订阅模块
            send_msg = SendMessage(self.token, self.AGENT_ID, self.msg_type, usr, content, '', '', '', '', '')
        else:
            # 用户主动发起的邮件模块
            send_msg = SendMessage(self.token, self.AGENT_ID, self.msg_type, usr, content, '', '', '', '', to_add)
        while True:
            if_success = send_msg.push_msg()
            if if_success == 1:
                break
            elif if_success == 0:
                # 推送失败基本就是token无效，重新获取即可
                f = open("token.txt", "w")
                self.token = GetToken(self.CORP_ID, self.SECRET, self.AGENT_ID).token
                f.write(self.token)
                f.close()
                if self.msg_type == 1:
                    send_msg = SendMessage(self.token, self.AGENT_ID, self.msg_type, usr, content, sub, ti,
                                           from_name, from_add, to_add)
                elif self.msg_type == 2:
                    send_msg = SendMessage(self.token, self.AGENT_ID, self.msg_type, usr, content, '', '', '', '', '')
                else:
                    send_msg = SendMessage(self.token, self.AGENT_ID, self.msg_type, usr, content, '', '', '', '',
                                           to_add)
            else:
                break


if __name__ == '__main__':
    push = ModulePush(2)
    push.read_local()
    push.wx_push('@all', '哪里出问题了？', '', '', '', '', '')
