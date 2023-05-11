import re

from WorkWX.ModulePush import *

'''
百度热搜模块封装好，无需改动，调用注意：
    1.如果不需要推送，直接 new 构造函数
    2.如果需要推送，new完执行push()
本模块适用于不提供XML文档的页面，具体代码根据具体页面会有不同
'''
class ModuleBaiduTop(object):
    def __init__(self):
        self.response = requests.get("https://top.baidu.com/board?tab=realtime")
        self.response.encoding = self.response.apparent_encoding
        # 解决编码问题，但仍有极小概率会出现乱码
        text = self.response.text  # 获取百度热榜HTML结构
        self.title = re.findall(r'query":"(.+?)",', text)
        self.urls = re.findall(r'"rawUrl":"(.+?)",', text)
        # 目前适用百度热榜的正则表达式，不清楚后面会不会改变页面结构，暂时不需改动
        self.content = ''
        self.lines = []
        for i in range(0, 15):
            self.lines.append("<a href=\"%s\">%s.%s</a>" % (self.urls[i + 1], str(i + 1), self.title[i + 1]))
            self.content = self.content + self.lines[i]
        f = open("baidu.txt", "w", encoding='utf-8')
        f.write(self.content)
        # 获取前十五条热搜，供前端页面读取展示，不进行群体推送

    def push(self):
        push = ModulePush(2)
        push.read_local()
        contents = "🎉此时百度热搜10条🎉\n"
        for i in range(0, 10):
            contents = contents + self.lines[i]
            if (i + 1) % 5 == 0:
                # 企业微信JSON长度限制，五条消息一组
                push.wx_push('@all', contents, '', '', '', '', '')
                contents = ""
                time.sleep(5)
                # 设置5秒间隔，防止因执行速度导致消息顺序错乱
            else:
                contents = contents + '\n'


if __name__ == '__main__':
    baidu = ModuleBaiduTop()
    baidu.push()
