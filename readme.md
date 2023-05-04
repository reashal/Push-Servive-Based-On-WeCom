## 项目介绍

### 开发目的

利用Python解析非腾讯系的第三方邮件系统未读邮件和RSS聚合订阅信息，以JSON的格式提交至企业微信接口，实现微信/企业微信消息推送的效果。同时考虑到消息推送可能会打断用户的专注，同时采用HTML、CSS、JavaScript和PHP实现数据的静默展示。

> 针对上述需求，如果使用官方APP，后台常驻容易造成性能浪费、越界获取权限可能会泄露隐私……如果使用网页，则可能会遇到需要频繁切换网页、重新登录和无休止的弹窗请求获取位置信息等场景。

### 开发成果

+ 邮件解析：
  + 用户仅需在第一次使用系统时填好邮箱信息，后续无需重新配置。
  + 系统按使用情景提供两种邮件拉取方式（网易流量限制的折中之计）：
    + 系统于特定时间段以特定频率拉取新邮件，适用于时效要求不高的日常沟通等邮件，如果没有新邮件则不进行提醒，避免过多无用的消息影响用户的工作和生活。
    + 用户点击按钮主动提交拉取请求，适合验证码接收等时效性较强的邮件，如果没有新邮件则会提示，用以告知用户系统处于正常工作状态。
  + 如果存在一天内的未读邮件，系统会依次将这些邮件的发件人、收件地址、时间、标题、正文概述等内容提取并进行精准推送，以便用户快速了解邮件内容。
+ 信息订阅：
  + 暂时只选取了百度热搜和开源中国这两个来源，其它RSS订阅源可参考项目代码按需开发。
  + 统截取每个订阅源的前十条内容，按顺序编号展示标题，点击即可查看具体内容。
  + 系统按需提供两种通知方式：
    + 于工作时间每隔三小时面向群体推送一次。
    + 每隔十分钟解析并生成网页，供用户按需点击查看。
+ 数据传递：
  + 后端各模块之间、前后端之间数据或采用文本方式传递纯文本内容、或严格按照文档配置JSON，数据传递简洁高效。采用CSS或模板卡片调整样式，跨平台、响应不同尺寸设备，使得信息展示美观清晰~~（前端样式是流式布局，表现细节懒得改了）~~。

### 成果展示

![微信推送效果](https://static.reashal.com/images/graduation/wechatpush.jpg)

![企业微信推送效果](https://static.reashal.com/images/graduation/workwxpush.jpg)

![手机端使用说明](https://static.reashal.com/images/graduation/mindex.jpg)

![手机端百度热搜](https://static.reashal.com/images/graduation/mbaidu.png)

![手机端开源中国](https://static.reashal.com/images/graduation/moschina.png)

![平板端百度热搜](https://static.reashal.com/images/graduation/padbaidu.png)

![电脑端使用说明](https://static.reashal.com/images/graduation/pcindex.jpg)

## 使用说明

### 开发环境

开发及测试环境为Windows 10系统，部署运行于CentOS 7.8系统，注重程序的可移植性，故项目采用跨平台语言实现（前端网页生成时用的PHP除外，因为最终运行于阿里云服务器，本身便配有PHP环境，作为锦上添花的功能，使用PHP可以少做一些工作），数据交互采用JSON网络传输和文件本地存储，迁移时几乎不必重新配置环境。

Python项目中必须包含一个 requirements.txt 文件，用于记录所有依赖包及其精确的版本号，以便于新环境部署。

+ 开发环境生成requirements.txt文件：
  + pip freeze > requirements.txt

+ 运行环境安装requirements.txt依赖：
  + pip install -r requirements.txt


### 项目结构

+ 本项目各模块已封装完毕，运行***Main.py*** 即可
  + Linux常驻后台运行：nohup python Main.py &

+ 各模块**最终封装成品(加粗)**及其它结构简介：
  + **邮件处理**：
    + **Mail包**，拉取一天内最新的未读邮件并在推送至微信/企业微信后将之自服务器删除。
    + **ModuleMail.py**
      + 对ReceiveMail功能的封装
    + ReceiveMail.py
  + **信息聚合**：
    + **RSS包**，解析此刻的订阅消息并将之推送至微信/企业微信。
    + **ModuleBaiduTop.py**
    + **ModuleOsChina.py**
  + **企微推送**：
    + **WorkWX包**，微信/企业微信消息推送，由上述两模块调用。
    + **ModulePush.py**
      + 对后续两个步骤的封装
    + GetToken.py
      + 企业微信其他API使用前必须先获取token
      + 请求频繁会被限制，所以优先读取缓存，若无效再去接口获取
    + SendMessage.py：
      + 获取token后就可以不间断发送连续消息了
  + **前端界面：**
    + **index.html**即系统使用说明，提供用户按需使用功能的按钮
    + mail.php
      + 创建pull_mail.txt，后端检测到会检查新邮件并处理
    + baidu.php
      + 后端每隔十分钟更新百度热搜十条，通过根目录baidu.txt传递后由本文件生成网页
    + oschina.php
      + 同上，根目录oschina.txt传递
  + **其他文件若干：**
    + pull_mail.txt
      + 服务器不能太频繁拉取邮件信息，否则会被限制流量，所以每隔5s判断是否有手动拉取邮件的需要就是看此文件是否存在，在则拉取推送，然后删除
    + token.txt
      + 不能太频繁通过企业微信接口获取token，否则会被限制，所以优先在此文件写入token缓存
    + requirements.txt
      + 环境部署所需，开篇提到

### 参数说明

* **Main.py**
  * 调用 **Mail.Module.Module(a)** 时，参数为1代表自动推送，不发送空邮件提醒，参数为2则代表手动拉取，提醒没有新邮件
  * 调用**RSS.ModuleBaituTop.ModuleBaiduTop()**，即可获取一次最新订阅，并将之展示到前端，**.push**则会推送
* **Mail/ModuleMail.py**
  * 调用**Mail.ReceiveMail.ReceiveMail()**的时，传入**邮箱登录所需信息**
* __Mail/ReceiveMail.py__
  * connect_mail()中 text = b'\r\n'.join(lines) 在不同操作系统中可能需要改(貌似不用)
  * get_mail_info()中第一个参数为企业微信企业成员ID
* **WorkWX/ModulePush.py**
  * **构造函数**配置**企业微信相关参数(使用前一次性配置)和推送的消息类型(调用时传参)**
* **Mail/SendMessage.py**
  * 构造函数对照企业微信官方api文档发送消息部分，可以更改消息模板

### 企微配置

文中提到的几个参数、自建应用、添加可信IP等均需配置。

![企业微信配置1](https://static.reashal.com/images/graduation/workwx1.png)

![企业微信配置2](https://static.reashal.com/images/graduation/workwx2.png)

![企业微信配置3](https://static.reashal.com/images/graduation/workwx3.png)

## 系统设计

本节给出系统结构设计图，随后依次展开对邮件、订阅和展示三个模块的设计。各模块开发步骤即围绕设计图展开，代码注释较多，在此不做赘述。

### 系统结构设计图

![系统结构设计图](https://static.reashal.com/images/graduation/module_system.png)

### 邮件模块设计图

![邮件模块设计图](https://static.reashal.com/images/graduation/module_mail.png)

### 订阅模块设计图

![订阅模块设计图](https://static.reashal.com/images/graduation/module_rss.png)

### 展示模块设计图

![展示模块设计图](https://static.reashal.com/images/graduation/module_display.png)

## 设计流程

本节依次展开邮件解析与数据展示的设计流程。

### 邮件解析流程图

![邮件解析流程图](https://static.reashal.com/images/graduation/flow_mail.png)

### 数据展示流程图

![数据展示流程图](https://static.reashal.com/images/graduation/flow_push.png)

## 注意事项

### 邮件模块注意事项

+ 项目选用POP3协议实现，与IMAP的具体区别不做赘述，以网易邮箱为例，诸多限制如下：

  + 仅允许Outlook、foxmail等知名客户端通过IMAP连接，这意味着我们无法使用IMAP协议来处理网易邮箱账户的邮件。

  + 限制单邮箱账户的连接流量，如果我们频繁使用IMAP协议或者POP3协议访问邮箱，会触发流量限制，导致服务商关闭连接，无法及时接收邮件。

  + 服务器带宽限制，如果我们频繁地使用IMAP协议连接，可能会导致服务器崩溃。
  + POP3解析完邮件后需要从服务器中删除，否则会重复解析。

+ 邮件分为标头和载荷（内容）部分，有如下情况需要处理：

  + 二者的编码和解码问题，不处理字符集可能会得到奇怪的结果
  + 载荷可能是嵌套的结构，需要递归处理，并且也有可能是HTML结构，需要正则提取

### 订阅模块注意事项

根据不同来源订阅信息是否提供XML文档的情况，订阅模块可以采用两种解析方案,具体解析结构和代码实现会因文档结构略有不同。

+ 当订阅源提供XML文件时，我们可以使用feedparser库来解析XML，该库可以将XML文件中的订阅源解析为一个Python对象，然后通过对象中的entry属性获取所需信息。
+ 当订阅源不提供XML文件时，我们可以通过requests库抓取其HTML结构，然后使用Python内置的re库，通过正则表达式来匹配HTML标签和属性，并从中提取所需信息。需要注意的是，此处也会涉及到编码的问题。

### 推送模块注意事项

+ 发送消息时需要进行异常处理，例如请求超时、请求错误等。
+ 发送消息时需要注意消息的长度，不同消息类型的长度限制不同。
+ 可以根据接口返回值中的errcode和errmsg字段来判断消息是否成功发送。若errcode为0，则表示发送成功；若errcode不为0，则表示发送失败，errmsg中包含错误信息。
+ 对企业微信接口进行一些操作时，需要尽可能使用缓存的access_token。
+ 当系统运行所在机器的IP产生变动时，需要及时在企业微信应用管理后台添加可信IP，否则会推送失败

## 题外之话

项目代码和文档至此基本算完成了，有些需要用到的知识也基本上是现学现做，技艺不精查阅资料也挺费功夫。

文档对于开发流程没有展开详细阐述，也许有空会逐渐完善（上一篇说择日再更的文章一不小心隔了三年）。开发过程中的磕磕绊绊均以注释的形式保留，也是对本项目动手实践的一个见证（POP3协议解析邮件部分的开发过程中借鉴过其他人的代码，但往往有各种各样的小问题，对于纯文本内容的解析与展示，本项目应该还算比较有参考价值）。感谢学习过程中，诸位的无私分享，希望以长足进步加入开源大家庭。