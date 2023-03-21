var ava = document.getElementById('ava');
var music = document.getElementById('music');
var now;
var left = document.getElementById('lleft');
var right = document.getElementById('rright');
var dep = 0;
var btn = document.getElementById('musicBtn');
function getTime() {
    now = music.currentTime;
    dep = Number(((now / 263.0) * 360)).toFixed(0);
    ava.style.transform = `rotate(${dep*10}deg)`;
    if (dep <= 180) {
        right.style.transform = `rotate(${dep}deg)`;
        left.style.transform = `rotate(0)`;
    }
    else {
        left.style.transform = `rotate(${dep - 180}deg)`;
        right.style.transform = `rotate(180px)`;
    }
}
btn.onclick = function () {
    if (music.paused) {
        music.play();
        btn.className = "iconfont icon-pause";
        setInterval(function () { getTime() }, 2);
    }
    else {
        music.pause();
        btn.className = "iconfont icon-play";
    }
}