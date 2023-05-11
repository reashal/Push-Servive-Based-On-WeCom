import feedparser

from WorkWX.ModulePush import *

'''
开源中国模块封装好，无需改动，调用注意：
    1.如果不需要推送，直接 new 构造函数
    2.如果需要推送，new完执行push()
本模块适用于提供XML文档的订阅，以开源中国为例，供参考
'''
class ModuleOsChina(object):
    def __init__(self):
        self.oschina = feedparser.parse('https://www.oschina.net/news/rss')
        self.num = 0
        self.content = ''
        self.lines = []
        for entry in self.oschina['entries']:
            self.lines.append("<a href=\"%s\">%s.%s</a>" % (entry['link'], str(self.num + 1), entry['title']))
            self.content = self.content + self.lines[self.num]
            if (self.num >= 9):
                break
            else:
                self.content = self.content + '\n'
            self.num += 1
        f = open("oschina.txt", "w", encoding='utf-8')
        f.write(self.content)
        # 获取前十五条热搜，供前端页面读取展示，不进行群体推送

    def push(self):
        push = ModulePush(2)
        push.read_local()
        contents = "🎉此时开源中国10条🎉\n"
        for i in range(0, 10):
            contents = contents + self.lines[i]
            if (i + 1) % 5 == 0:
                push.wx_push('@all', contents, '', '', '', '', '')
                contents = ""
                time.sleep(5)
                # 设置5秒间隔，防止因执行速度导致消息顺序错乱
            else:
                contents = contents + '\n'


if __name__ == '__main__':
    oschina = ModuleOsChina()
    oschina.push()
