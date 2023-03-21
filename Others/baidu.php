<!DOCTYPE html>
<html lang="chn">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport"
        content="width=device-width,initial-scale=1.0,maximum-scale=1.0,minimum-scale=1.0,user-scalable=no">
    <title>即刻百度热搜</title>
    <meta name="author" content="reashal">
    <meta name="description" content="睿屿青衫个人导航页">
    <link rel="stylesheet" href="css/style.css">
    <link rel="shortcut icon" href="images/reashal.png">
    <link rel="stylesheet" href="//at.alicdn.com/t/c/font_3966102_mj8w76tpoa.css" </head>

<body>
    <div class="Explain" id="Explain">
        <span></span>
        <span></span>
        <span></span>
        <span></span>
        <i class="iconfont icon-play" id="musicBtn" title="播放音乐"></i>
        <a href="//des.reashal.com" target="_self"><i class="iconfont icon-planet" id="planet" title="回到主页"></i></a>
        <a href="//bak.reashal.com/projects/206b" target="_blank"><i class="iconfont icon-plane" id="plane" title="食用指南"></i></a>
        <input id="ifExplain" value="0">
    </div>
    <div class="card">
        <div class="rss">
            <h2 id="cnt">🎉此时百度热搜10条🎉</h2>
            <?php
                $file=fopen("../baidu.txt","r");
                while(!feof($file))
                {
                    echo fgets($file);
                }
                fclose($file);
            ?>
            <div class="fff"></div>
        </div>
    </div>
    <div class="footer">
        <p class="copy">reashal &copy 2023</p>
    </div>
    <!--鼠标点击泡泡特效，网上找的-->
    <canvas class="fireworks" style="position:fixed;left:0;top:0;z-index:99999999;pointer-events:none;"></canvas>
    <script type="text/javascript" src="js/djtx.js"></script>
    <!-- 音乐通过头像由JS控制 -->
    <audio controls id="music" class="music" loop>
        <source src="music/LettingGo.mp3" type="audio/mpeg">
    </audio>
    <script src="js/avator.js" async="async"></script>
    <!-- JS异步，加载完DOM再操作，否则可能报错 -->
    <script src="js/about.js" async="async"></script>
</body>

</html>