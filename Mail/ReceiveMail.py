import re
import poplib
from email.parser import Parser
from Others.GetTime import GetTime
from email.utils import parseaddr
from email.header import decode_header

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
  构造函数的参数
  connect_mail()中text = b'\r\n'.join(lines)
  get_mail_info()中第一个参数为企业微信用户id
'''


class ReceiveMail(object):
    def __init__(self, usr, pwd, host, port):
        self.usr = usr
        self.pwd = pwd
        self.host = host
        self.port = port
        self.content = ''
        self.if_a_mail = self.connect_mail()

    def if_have_mail(self):
        # 第二步
        # print(self.if_a_mail)
        return self.if_a_mail

    def get_text_charset(self, text):
        # 第五步，重新编码，否则非utf-8编码的邮件无法正常显示
        # 获取编码
        charset = text.get_charsets()[0]
        '''
        email.message
        返回一个包含了信息内所有字符集名字的列表。
          如果信息是 multipart 类型的，那么列表当中的每一项都对应其载荷的子部分的字符集名字。

          否则，该列表是一个长度为 1 的列表。
          列表当中的每一项都是一个字符串，其值为对应子部分的 Content-Type 头字段的 charset 参数值。
          如果该子部分没有此头字段，或者没有此参数，或者其主要 MIME 类型并非 text ，那么列表中的那一项即为 failobj 。
        '''
        # 最内层载荷才会调用该函数，这边意味着非multiple类型，即上面三条注释
        return charset

    def decode_str(self, header):
        # 第四步 标头部分内容的解码
        '''
        email.header.decode_header(header)
        在不转换字符集的情况下对消息标头值进行解码。header为标头值
        返回一个 (decoded_string, charset)对的列表，
          其中包含标头的每个已解码部分。
          对于标头的未编码部分 charset 为 None，
          在其他情况下则为一个包含已编码字符串中所指定字符集名称的小写字符串。
        '''
        decoded_string, charset = decode_header(header)[0]
        if charset:
            decoded_string = decoded_string.decode(charset)
        return decoded_string

    def get_final_content(self, text):
        # 第六步，邮件正文可能是复杂冗长的html结构，企业微信不支持此类代码的推送
        # 剔除形如<...>的标签，未被<>包裹的即为所需正文
        con = re.sub(r'<style>(.+?)</style>', '\n', text)
        con = re.sub(r'<(.+?)>', '\n', con)
        con = re.sub(r'&(.+?);', '\n', con)
        '''
          <.+?> 中?表示懒惰模式，从<开始到第一个>结束匹配
          <.+>则是非懒惰模式，到最后一个>结束匹配
        '''
        #   1.去掉CSS样式，换成空行
        #   2.去掉标签，换成空行
        #   3.此时的字符串可能还有一堆空行，去除HTML中几个转义的空格符号
        # print(con)
        con = con.splitlines()
        # 将包含正文、无用分隔符的字符串按行分割为列表，不保留换行符
        # print(con)
        fin_content = ' | '
        # 企业微信传递内容空间有限，用此符号代替换行
        for i in con:
            if i != '':
                fin_content = fin_content + i + ' | '
        self.content = fin_content

    def get_mail(self, text, num):
        # 第三步，解析邮件内容
        '''
        email.message

        一份电子邮件信息由 标头 和 载荷（内容）组成

        标头
          格式为 "字段名" : "字段值"
              一次性获取即可，处理键值对

        载荷
          可能是一段简单的文字消息，
          可能是一个二进制的对象，
          可能是由多个拥有各自标头和载荷的子信息组成的结构化子信息序列
              可能需要递归处理，直至获取到所需内容
        '''
        # 处理标头, 不需要循环，第一次即可获取
        if num == 0:
            # print(text)
            '''
              里面内容很多，标头需要用到以下前三条，文本可能需要最后一条：
                  From: "=?gb18030?B?7qPT7MfgycA=?=" <ruiyuqingshan@vip.qq.com>
                  To: "=?gb18030?B?Nzc3OTAw?=" <777900@163.com>
                  Subject: =?gb18030?B?tdq2/rfi?=
                  Content-Type: text/plain; charset="gb18030"
            '''
            # 后期设置只取一两天内新邮件，输出数据忘记写在上面了
            '''
                email.utils.parseaddr(address)
                将地址（诸如To之类包含地址的字段）值解析为构成之的 真实名字 和 电子邮件地址 部分。
                返回包含这两个信息的一个元组；如若解析失败，则返回一个二元组 ('', '')
            '''
            mail_from = text.get('From', '')
            mail_from = parseaddr(mail_from)
            self.from_add = mail_from[1]
            # 发件人邮箱
            self.from_name = self.decode_str(mail_from[0])
            # 发件人用户名
            # 邮件中的名字经过编码，需要解码后才能正常显示
            self.to_add = parseaddr(text.get('To', ''))[1]
            # 收件人邮箱
            self.sub = self.decode_str(text.get('Subject', ''))
            # 邮件标题也是经过编码的，也需要解码
            self.ti = text.get('Date').split(' ')
            self.day = self.ti[1]
            if int(self.day) + 1 < int(GetTime().get_day()):
                return 0

        # 处理载荷
        '''
        email.parser
        所有 multipart 类型的消息都会被解析成一个容器消息对象。
        该对象的负载是一个子消息对象列表。
        外层的容器消息在调用 is_multipart() 的时候会返回 True ，
        在调用 iter_parts() 的时候会产生一个子部分列表。

        大多数内容类型为 message/* （例如 message/delivery-status 和 message/rfc822 ）的消息也会被解析为一个负载是长度为1的列表的容器对象。
        在它们身上调用 is_multipart() 方法会返回 True ，
        调用 iter_parts() 所产生的单个元素会是一个子消息对象。
        '''
        if text.is_multipart():
            # 循环找最里层嵌套的消息对象
            lists = text.get_payload()
            # 返回list，包含所有的子对象
            # print(lists)
            #   [<email.message.Message object at 0x031DD5B0>, <email.message.Message object at 0x03350280>]

            for index, ele in enumerate(lists):
                # 将list里边索引和元素枚举出来
                '''
                enumerate(sequence, [start = 0])
                  sequence -- 一个序列、迭代器或其他支持迭代对象
                  start -- 下标起始位置的值
                返回 enumerate(枚举) 对象
                '''
                self.get_mail(ele, num + 1)

            '''
            大多数非 multipart 类型的消息都会被解析为一个带有字符串负载的消息对象。
            这些对象在调用 is_multipart() 的时候会返回 False ，
            调用 iter_parts() 的时候会产生一个空列表。
            '''
        else:

            '''
            返回信息的内容类型，其形如 maintype/subtype ，强制全小写。
              如果信息的 Content-Type 头字段不存在则返回 get_default_type() 的返回值；
              如果信息的 Content-Type 头字段无效则返回 text/plain 。
              根据 RFC 2045 所述，信息永远都有一个默认类型，所以 get_content_type() 一定会返回一个值。
              RFC 2045 定义信息的默认类型为 text/plain 或 message/rfc822 ，其中后者仅出现在消息头位于一个 multipart/digest 容器中的场合中。
              如果消息头的 Content-Type 字段所指定的类型是无效的， RFC 2045 令其默认类型为 text/plain
            '''
        content_type = text.get_content_type()
        # if content_type == 'text/plain' or content_type == 'text/html':
        if content_type == 'text/html':
            # 企业微信文本卡片消息需要提取文本内容
            contents = text.get_payload(decode=True)
            # print(lists)
            '''
            # 返回list，包含所有的子对象
            #   [<email.message.Message object at 0x031DD5B0>, <email.message.Message object at 0x03350280>]
            '''
            charset = self.get_text_charset(text)
            # 第五步，重新编码，否则非utf-8编码的邮件无法正常显示
            if charset:
                contents = contents.decode(charset)
                contents = contents.replace('    ', '')
                contents = contents.replace('\r\n', '')
                # 有时获取的邮件是HTML格式，先去掉缩进，使每行左对齐
                # print(contents)
                self.get_final_content(contents)
                # 第六步，邮件正文可能是复杂冗长的html结构，企业微信不支持此类代码的推送
                # 剔除形如<...>的标签，未被<>包裹的即为所需正文
                # print(self.content)
        else:
            pass
            # 企业微信文本卡片消息仅需要提取邮件正文文本即可，其他无法传递，跳过

    def connect_mail(self):
        # 第一步，连接邮箱
        try:
            server = poplib.POP3(self.host, self.port)
            server.user(self.usr)
            server.pass_(self.pwd)
        except:
            print("邮箱登录失败")
            print("请按序重新检查以下信息：邮箱地址|邮箱授权码|POP服务器地址|端口号")
            print("授权码并非邮箱登录密码，需到邮箱设置里生成保存，并开启POP3协议")

        # print(server.stat())
        if (server.stat()[0] == 0):
            # 第二步，如果没有邮件就停止后续工作
            print("目前没有新邮件，已经发送提醒")
            return 0
        # 输出 (消息数量,邮箱大小)，则邮箱连接成功

        res, mails, octs = server.list()
        # print(server.list())
        '''
          输出(b'+OK 2 7045', [b'1 3551', b'2 3494'], 16)
          格式(response, ['mesg_num octets', ...], octets)
        '''
        # print(mails)
        '''
          mails为获得的消息列表，索引从1开始
          [b'1 3551', b'2 3494']
        '''

        res, lines, octs = server.retr(len(mails))
        '''
        获取最新一封邮件
          每一个line都是原始邮件文本的一整行,字节类型
        print(server.retr(len(mails)))
          (response, ['line', ...], octets)
        print(lines[0])
          输出b'Received: from xmbg7.mail.qq.com (unknown [101.91.43.96])'
        '''
        # print(type(lines[0]))

        text = b'\r\n'.join(lines)
        # win用'\r\n'，Linux用'\n'来给字节 b'' 换行
        # 然后join生成一个新字节串

        text = text.decode('utf-8','ignore')
        # 将 字节 编码为 utf-8 字符串

        text = Parser().parsestr(text)
        # 从text读取所有数据，解析所读取的文本，并返回消息对象
        #   返回 email.message.Message

        self.get_mail(text, 0)
        # 第三步，解析邮件内容

        server.dele(len(mails))
        # 第七步，删除邮件

        server.quit()
        # 最后，关闭邮箱连接

        return 1

    def get_from_add(self):
        return self.from_add

    def get_from_name(self):
        return self.from_name

    def get_to_add(self):
        return self.to_add

    def get_sub(self):
        return self.sub

    def get_content(self):
        return self.content

    def get_day(self):
        return self.day

    def get_mail_info(self):
        self.ti = "%s%s日 %s" % (GetTime().get_time(), self.ti[1], self.ti[4])
        return ['ruiyuqingshan', self.content, self.sub, self.ti, self.from_name, self.from_add, self.to_add]
