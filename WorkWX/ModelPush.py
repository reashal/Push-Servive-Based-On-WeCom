from WorkWX.GetToken import *
from WorkWX.SendMessage import *

'''
封装好的企业微信推送模块思路
第一次先获取token（本地/接口）
验证token后 直接连续推送内容
'''


# 后期可能需要改这里

class ModelPush:
    def __init__(self, msg_type):
        # 已封装好，企业微信相关信息只改这里即可
        # 参数如果是1代表主动推送邮件
        # 参数如果是2代表RSS的普通文本消息
        # 参数如果是3代表手动拉取邮件
        self.CORP_ID = "111"  # 我的企业 企业ID
        self.SECRET = "111"  # 自建应用SECRET
        self.AGENT_ID = "111"  # 自建应用AgentId
        self.token = "0" # 初始化，值随意
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

        if self.msg_type == 1:
            send_msg = SendMessage(self.token, self.AGENT_ID, self.msg_type, usr, content, sub, ti,
                                   from_name, from_add, to_add)
        elif self.msg_type == 2:
            send_msg = SendMessage(self.token, self.AGENT_ID, self.msg_type, usr, content, '', '', '', '', '')
        else:
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
    push = ModelPush(2)
    push.read_local()
    push.wx_push('@all', '哪里出问题了？', '', '', '', '', '')
