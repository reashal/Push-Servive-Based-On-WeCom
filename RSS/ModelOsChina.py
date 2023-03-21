import feedparser

from WorkWX.ModelPush import *


class ModelOsChina(object):
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

    def push(self):
        push = ModelPush(2)
        push.read_local()
        contents = "🎉此时开源中国10条🎉\n"
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
    oschina = ModelOsChina()
    oschina.push()
