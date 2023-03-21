import re

from WorkWX.ModelPush import *


class ModelBaiduTop(object):
    def __init__(self):
        self.response = requests.get("https://top.baidu.com/board?tab=realtime")
        self.response.encoding = self.response.apparent_encoding  # 中文乱码问题
        text = self.response.text  # 获取百度热榜HTML结构

        self.title = re.findall(r'query":"(.+?)",', text)
        self.urls = re.findall(r'"rawUrl":"(.+?)",', text)
        # 目前适用百度热榜的正则表达式，不清楚后面会不会改变页面结构
        self.content = ''
        self.lines = []
        for i in range(0, 15):
            self.lines.append("<a href=\"%s\">%s.%s</a>" % (self.urls[i + 1], str(i + 1), self.title[i + 1]))
            self.content = self.content + self.lines[i]
        f = open("baidu.txt", "w", encoding='utf-8')
        f.write(self.content)

    def push(self):
        push = ModelPush(2)
        push.read_local()
        contents = "🎉此时百度热搜10条🎉\n"
        for i in range(0, 10):
            contents = contents + self.lines[i]
            if (i + 1) % 5 == 0:
                push.wx_push('@all', contents, '', '', '', '', '')
                contents = ""
                time.sleep(2)
                # 设置2秒间隔，防止消息顺序错乱
            else:
                contents = contents + '\n'


if __name__ == '__main__':
    baidu = ModelBaiduTop()
    baidu.push()
