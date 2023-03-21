## 项目介绍

#### 🎉开发目的🎉

长话短说，为了在微信上收到及时的未读邮件提醒和订阅信息推送，免安装多余APP

#### 🎉开发结果🎉

+ 定时任务：每天8~20时，通过微信/企业微信发送推送
  + 每隔15分钟拉取一次邮件，原本预计5s的频率被163制裁多次了
    + 有邮件则通知
    + 没有邮件不通知
  + 每隔3小时推送一次最新订阅
    + 百度热搜
    + 开源中国
+ 手动任务：不限制时间，在前端页面展示
  + 在5s内于企业微信返回新邮件信息，没有也会提示
  + 每隔10分钟获取一次订阅，百度热搜/开源中国


#### 🎉使用须知/手动任务🎉

**index.html**,短期内[这里](https://des.reashal.com)可以展示前端页面

#### 🎉效果展示🎉

![微信推送](https://images.reashal.com/design/WX.jpg)

![企业微信推送](https://images.reashal.com/design/WorkWX.jpg)

![项目使用说明](https://images.reashal.com/design/read.jpg)

## 项目构成

#### 🎉环境🎉

python项目中必须包含一个 requirements.txt 文件，用于记录所有依赖包及其精确的版本号。以便新环境部署

+ 生成requirements.txt文件：pip freeze > requirements.txt
+ 安装requirements.txt依赖：pip install -r requirements.txt

#### 🎉结构总览(package)🎉

+ 本项目各模块已封装完毕，运行***Main.py*** 即可
+ 各功能 **最终封装成品(加粗)** 及其他结构功能简介：
  + **邮件处理**：**Mail包**，拉取最新的未读邮件并在推送至微信/企业微信后删除
    + **ModelMail.py**
      + 对ReceiveMail功能的封装
    + ReceiveMail.py
  + **信息聚合**：**RSS包**，解析此刻的订阅消息并推送至微信/企业微信
    + **ModelBaiduTop.py**
    + **ModelOsChina.py**
  + **企微推送**：**WorkWX包**，微信/企业微信消息推送，由上述两模块调用
    + **ModelPush.py**
    + GetToken.py
      + 企业微信其他API使用前必须先获取token
      + 请求频繁会被限制，所以优先读取缓存，若无效再去接口获取
    + SendMessage.py：
      + 获取token后就可以不间断发送连续消息了
  + 其他文件
    + **GetTime.py**：Others包，获取当前时间，邮件发送模板卡片消息会调用
    + 若干前端所需文件
  + **前端界面：index.html**
    + 包含项目使用说明、手动拉取功能
    + mail.php
      + 创建pull_mail.txt，后端检测到会检查新邮件
    + baidu.php
      + 百度热搜十条，每隔十分钟更新一次，通过根目录baidu.txt传递
    + oschina.php
      + 同上，根目录oschina.txt传递
  + **其他文件：**
    + pull_mail.txt
      + 服务器不能太频繁拉取邮件信息，否则会被限制流量，所以每隔5s判断是否有手动拉取邮件的需要就是看此文件是否存在，在则拉取推送，然后删除
    + token.txt
      + 不能太频繁通过企业微信接口获取token，否则会被限制，所以优先在此文件写入token缓存
    + requirements.txt
      + 环境部署所需，开篇提到

#### 🎉调用/修改说明🎉

* **Main.py**
  * 调用 **Mail.Model.Model(a)** 时，参数为1代表自动推送，不发送空邮件提醒，参数为2则代表手动拉取，提醒没有新邮件
  * 调用**RSS.ModelBaituTop.ModelBaiduTop()**，即可获取一次最新订阅，并将之展示到前端，**.push**则会推送
* **Mail/ModelMail.py**
  * 调用**Mail.ReceiveMail.ReceiveMail()**的时，传入**邮箱登录所需信息**
* __Mail/ReceiveMail.py__
  * connect_mail()中 text = b'\r\n'.join(lines) 在不同操作系统中可能需要改(貌似不用)
  * get_mail_info()中第一个参数为企业微信企业成员ID
* **WorkWX/ModelPush.py**
  * **构造函数**配置**企业微信相关参数(使用前一次性配置)和推送的消息类型(调用时传参)**
* **Mail/SendMessage.py**
  * 构造函数对照企业微信官方api文档发送消息部分，可以更改消息模板

#### 🎉企业微信相关配置🎉

文中提到的几个参数，自建应用，添加可信IP，添加菜单等……


## 后话

目前大概都完成了，有些需要用到的东西也基本上是现学现做，技艺不精查资料也挺费工夫。

注释保留了实现过程的磕磕绊绊，感谢学习过程中各位的分享，希望以长足进步加入开源大家庭。