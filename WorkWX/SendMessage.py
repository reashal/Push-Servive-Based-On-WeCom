import time

import requests


# 验证token有效后进行消息发送
# 此处为不同消息类型的JSON推送模板，可以按需改动，但一定要严格参考企业微信官方提供的格式

class SendMessage(object):

    def __init__(self, token, agent_id, msg_type, user, content, sub, ti, from_name, from_add, to_add):
        self.msg_type = msg_type
        self.url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s" % token
        if msg_type == 1:
            # 新邮件提醒
            self.data = {
                "touser": user,
                # 个人/部门/标签三选一，不得全部为空
                "msgtype": "text",
                "agentid": agent_id,
                "text": {
                    "content": "🎉您收到了一封新邮件🎉\n🔔《%s》\n📃：“%s”\n✍：%s<%s>\n📫%s\n✨可进企业微信查看模板卡片消息\n🎉本邮件已自动删除，可以进入[您的官方邮箱-客户端删信]中查看原邮件" % (
                        sub, content, from_name, from_add, to_add)},
                "safe": "0"
            }
            self.data2 = {
                "touser": user,
                "msgtype": "template_card",
                "agentid": agent_id,
                "template_card": {
                    "card_type": "text_notice",
                    "source": {
                        "icon_url": "https://images.reashal.com/resources/avator/reashal.png",
                        "desc": "您收到了一封新邮件",
                        "desc_color": 2  # 来源文字的颜色，目前支持：0(默认) 灰色，1 黑色，2 红色，3 绿色
                    },
                    "main_title": {
                        "title": "《%s》" % sub,
                        "desc": ti
                    },
                    "quote_area": {
                        "type": 1,
                        "url": "https://www.reashal.com/posts/post-011",
                        "title": "邮件内容：",
                        "quote_text": content
                    },
                    "sub_title_text": "|官方邮箱-客户端删信|可以查看详情",
                    "horizontal_content_list": [
                        {
                            "keyname": "发件人",
                            "value": from_name
                        },
                        {
                            "type": 1,
                            "keyname": "发件邮箱",
                            "value": from_add,
                            "url": "mail:%s" % from_add
                        },
                        {
                            "type": 1,
                            "keyname": "收件邮箱",
                            "value": to_add,
                            "url": "mail:%s" % to_add
                        },
                    ],
                    "jump_list": [
                        {
                            "type": 1,
                            "title": "点击查看使用须知",
                            "url": "https://des.reashal.com"

                        }
                    ],
                    "card_action": {
                        "type": 1,
                        "url": "https://www.reashal.com/posts/post-011",
                    }
                },
            }
        elif msg_type == 2:
            # RSS推送
            self.data = {
                "touser": user,
                # 个人/部门/标签三选一，不得全部为空
                "msgtype": "text",
                "agentid": agent_id,
                "text": {"content": content},
                "safe": "0"
            }
        else:
            # 目前没有新邮件
            self.data = {
                "touser": user,
                # 个人/部门/标签三选一，不得全部为空
                "msgtype": "text",
                "agentid": agent_id,
                "text": {
                    "content": "🎉目前没有新邮件🎉\n📫%s" % to_add},
                "safe": "0"
            }

    def push_msg(self):
        if self.msg_type == 1:
            req = requests.post(url=self.url, json=self.data)
            json = req.json()
            flag = 0;
            if json['errcode'] == 0:
                print("本条文本消息推送成功，微信/企业微信可见")
                flag += 1
            else:
                print("本条文本消息[1]推送失败，正在重试")
            time.sleep(1)
            req2 = requests.post(url=self.url, json=self.data2)
            json2 = req2.json()
            if json2['errcode'] == 0:
                print("本条模板卡片消息推送成功，仅企业微信可见")
                flag += 1
            else:
                print("本条消息推送失败，正在重试")
            if flag == 2:
                print("新邮件两种通知均已成功推送")
                return 1
            print("新邮件两种通知未全部推送")
            return 0
        elif self.msg_type == 2:
            req = requests.post(url=self.url, json=self.data)
            json = req.json()
            if json['errcode'] == 0:
                # 企业微信提供的出错返回码
                print("本条文本消息推送成功，微信/企业微信可见")
                return 1
            else:
                print("本条文本消息[2]推送失败，正在重试")
                return 0
        elif self.msg_type == 3:

            req = requests.post(url=self.url, json=self.data)
            json = req.json()
            if json['errcode'] == 0:
                print("本条文本消息推送成功，微信/企业微信可见")
                return 1
            else:
                print("本条文本消息[3]推送失败，正在重试")
                return 0
        else:
            print("参数传递错误：")
            print("1代表新邮件通知，2代表消息订阅推送，3代表无新邮件提醒")
            return -1
