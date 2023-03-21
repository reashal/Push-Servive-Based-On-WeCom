import requests


# 企业微信消息推送需要首先获取 token
# 已封装完毕

class GetToken(object):

    def __init__(self, corp_id, secret, agent_id):
        self.corp_id = corp_id  # 我的企业 企业ID
        self.secret = secret  # 自建应用SECRET
        self.agent_id = agent_id  # 自建应用AgentId
        self.token = self.get_token()  # token下一步验证

    def get_token(self):
        '''
        获取access_token相当于创建了一个登录凭证，其它的业务API接口，都需要依赖于access_token来鉴权调用者身份。
        每个应用有独立的secret，获取到的access_token只能本应用使用
        '''
        url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (self.corp_id, self.secret)
        req = requests.get(url)
        # 返回 response 对象
        # print(res.content)
        json = req.json()
        # 返回结果的 JSON 对象
        if json['errcode'] == 0:  # 出错返回码，为0表示成功，非0表示调用失败
            print("本次token为接口获取")
            return json["access_token"]
        else:
            return "0"  # 获取token失败
