var shuoming = document.getElementById('shuoming');
shuoming.onclick = function () {
    var ifExplain = document.getElementById('ifExplain');
    var card = document.getElementById('flexBox');;
    if (ifExplain.value == 0) {
        card.className = 'flexBox-flip';
        ifExplain.value = '1';
        shuoming.title = '回到主页'
    }
    else {
        card.className = 'flexBox-back';
        ifExplain.value = '0';
        shuoming.title = '查看介绍'
    }

}