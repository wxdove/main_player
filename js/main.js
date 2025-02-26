// 获取主题背景
var body = document.getElementById('body');
const backgrounds = [
    './img/bg1.png',
    './img/bg2.png',
    './img/bg3.png',
    './img/bg4.jpg',
    './img/bg5.jpg',
    './img/bg6.jpg',
    './img/bg8.jpg',
    './img/bg9.jpg',
    './img/bg10.jpg',
    './img/bg11.jpg',
];
// 获取衣服图标元素
const shirtIcon = document.getElementById("shirt-icon");
// 当前背景图片索引
let currentBackgroundIndex = 0;
// 给衣服图标绑定点击事件
shirtIcon.addEventListener("click", () => {
    // 递增索引，确保背景图片切换
    currentBackgroundIndex = (currentBackgroundIndex + 1) % backgrounds.length;

    // 更新背景图片
    body.style.backgroundImage = `url('${backgrounds[currentBackgroundIndex]}')`;
});
// 获取音频播放器对象
var main = document.getElementById('audioTag');
// 歌曲名
var musicTitle = document.getElementById('music-title');
// 歌曲海报
var recordImg = document.getElementById('record-img');
// 歌曲作者
var author = document.getElementById('author-name');
// 进度条
var progress = document.getElementById('progress');
// 总进度条
var progressTotal = document.getElementById('progress-total');
// 已进行时长
var playedTime = document.getElementById('playedTime');
// 总时长
var audioTime = document.getElementById('audioTime');
// 播放模式按钮
var mode = document.getElementById('playMode');
// 确保 DOM 加载完成后再获取元素
window.addEventListener('DOMContentLoaded', function () {
    var skipForward = document.getElementById('skipForward');
    var skipBackward = document.getElementById('skipBackward');

    // 上一首按钮事件
    skipForward.addEventListener('click', function (event) {
        musicId = (musicId - 1 + musicListData.length) % musicListData.length;
        initAndPlay(musicListData[musicId]);
    });

    // 下一首按钮事件
    skipBackward.addEventListener('click', function (event) {
        musicId = (musicId + 1) % musicListData.length;
        initAndPlay(musicListData[musicId]);
    });
});
// 暂停按钮
var pause = document.getElementById('playPause');
// 音量调节
var volume = document.getElementById('volume');
// 音量调节滑块
var volumeTogger = document.getElementById('volumn-togger');
// 列表
var list = document.getElementById('list');
// 倍速
var speed = document.getElementById('speed');
// 音乐列表面板
var musicList = document.getElementById('music-list');
// 暂停/播放功能实现
pause.onclick = function (e) {
    if (main.paused) {
        main.play();
        rotateRecord();
        pause.classList.remove('icon-play');
        pause.classList.add('icon-pause');
    } else {
        main.pause();
        rotateRecordStop();
        pause.classList.remove('icon-pause');
        pause.classList.add('icon-play');
    }
}
// 更新进度条
main.addEventListener('timeupdate', updateProgress); // 监听音频播放时间并更新进度条
function updateProgress() {
    var value = main.currentTime / main.duration;
    progress.style.width = value * 100 + '%';
    playedTime.innerText = transTime(main.currentTime);
}
//音频播放时间换算
function transTime(value) {
    var time = "";
    var h = parseInt(value / 3600);
    value %= 3600;
    var m = parseInt(value / 60);
    var s = parseInt(value % 60);
    if (h > 0) {
        time = formatTime(h + ":" + m + ":" + s);
    } else {
        time = formatTime(m + ":" + s);
    }

    return time;
}
// 格式化时间显示，补零对齐
function formatTime(value) {
    var time = "";
    var s = value.split(':');
    var i = 0;
    for (; i < s.length - 1; i++) {
        time += s[i].length == 1 ? ("0" + s[i]) : s[i];
        time += ":";
    }
    time += s[i].length == 1 ? ("0" + s[i]) : s[i];

    return time;
}
// 点击进度条跳到指定点播放
progressTotal.addEventListener('mousedown', function (event) {
    // 只有音乐开始播放后才可以调节，已经播放过但暂停了的也可以
    if (!main.paused || main.currentTime != 0) {
        var pgsWidth = parseFloat(window.getComputedStyle(progressTotal, null).width.replace('px', ''));
        var rate = event.offsetX / pgsWidth;
        main.currentTime = main.duration * rate;
        updateProgress(main);
    }
});
list.addEventListener('click', function(event) {
    event.stopPropagation(); // 阻止点击事件冒泡
    // 切换音乐列表显示状态
    if (musicList.style.display === "none" || musicList.style.display === "") {
        musicList.style.display = "flex";
    } else {
        musicList.style.display = "none";
    }
});
// 监听全局点击事件，隐藏音乐列表
document.addEventListener('click', function(event) {
    // 判断点击的是否是 #music-list 或 #list 按钮
    if (!musicList.contains(event.target) && event.target !== list) {
        musicList.style.display = "none";
    }
});
// 存储当前播放的音乐序号
var musicId = 0;
// 获取元素
var searchInput = document.getElementById('searchInput');
var searchBtn = document.getElementById('searchBtn');
var resultsContainer = document.getElementById('music-items');
var apiSelect = document.getElementById('apiSelect');
var musicListData = [];
searchBtn.addEventListener('click', function() {
    var query = searchInput.value.trim();
    var selectedApi = apiSelect.value;

    if (query) {
        if (selectedApi) {
            searchMusic(query, selectedApi);  // 进行音乐搜索
        } else {
            alert('Please select a music source!');
        }
    } else {
        alert('Please enter a search term!');
    }
});
// 显示或隐藏加载动画
const showLoading = (show) => {
  resultsContainer.innerHTML = show ?
    `<div class="loading"><i class="fas fa-spinner fa-spin"></i> 正在努力搜索...</div>`
    : '';
};
// 监听搜索按钮点击事件
document.getElementById('searchBtn').addEventListener('click', async () => {
    showLoading(true); // 显示加载动画
    // 模拟异步搜索请求（这里可以替换为真正的API请求）
    setTimeout(() => {
        resultsContainer.innerHTML = '<p>马上找到啦...</p>'; // 显示搜索结果
    }, 4000);
});
// 渲染音乐列表到页面
function renderMusicList(songs) {
    console.log('Rendering music list:', songs);  // 打印出歌曲列表，检查数据结构

    if (songs.length === 0) {
        resultsContainer.innerHTML = '<p>No results found.</p>';
        return;
    }

    // 渲染歌曲项
    resultsContainer.innerHTML = songs.map((song, index) => {
        console.log('Rendering song:', song);  // 打印每一首歌，检查是否包含必要字段
        return `
            <div class="music-item" data-index="${index}" data-url="${song.play_url}" data-title="${song.SongName}" data-artist="${song.SingerName}" data-cover="${song.img}" data-lyrics="${song.lyrics}">
                <div class="music-info">
                    <h4>${song.SongName}</h4>
                    <p>${song.SingerName}</p>
                </div>
            </div>
        `;
    }).join('');  // 将所有歌曲项连接成一个字符串并渲染

    // 给每个音乐项添加点击事件，点击后播放该音乐
    var musicItems = document.querySelectorAll('.music-item');
    musicItems.forEach(item => {
        item.addEventListener('click', function() {
            var songIndex = this.getAttribute('data-index');
            var song = songs[songIndex];  // 使用传入的 songs 数组
            console.log('Song clicked:', song);  // 打印点击的歌曲信息
            initAndPlay(song);  // 播放点击的歌曲并更新UI
        });
    });
}
function searchMusic(query, source) {
    var url = '';
    if (source === 'search1') {
        url = `http://127.0.0.1:5000/search1?q=${query}`;  // 网易云音乐的假设API
    } else if (source === 'search2') {
        url = `http://127.0.0.1:5000/search2?q=${query}`;  // 酷狗音乐的假设API
    } else if (source === 'search3') {
        url = `http://127.0.0.1:5000/search3?q=${query}`;  // 酷狗音乐的假设API
    }

    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('API Data:', data);  // 打印 API 返回的数据，检查数据格式
            if (data.songs && Array.isArray(data.songs)) {
                musicListData = data.songs;  // 获取歌曲数据
                renderMusicList(musicListData);  // 渲染歌曲列表
            } else {
                console.error('No songs found in the response.');
                resultsContainer.innerHTML = '<p>No results found.</p>';
            }
        })
        .catch(error => {
            console.error('Error fetching music:', error);
            resultsContainer.innerHTML = '<p>Error fetching music. Please try again later.</p>';
        });
}
function initMusic(music) {
    if (!music) return;  // 如果没有音乐信息，直接返回
    main.src = music.play_url;  // 设置播放链接
    main.load();  // 重新加载音频
    // 更新 UI 显示歌曲信息
    musicTitle.innerText = music.SongName;  // 显示歌曲名称
    author.innerText = music.SingerName;  // 显示歌手名称
    recordImg.style.backgroundImage = `url('${music.img}')`; // 设置封面

    // 解析歌词并更新歌词数组
    lyrics = parseLyrics(music.lyrics);  // 解析歌词
    // 如果有歌词，显示到页面
    let lyricsContainer = document.getElementById("lyrics-container");
    if (lyricsContainer) {
        lyricsContainer.innerText = music.lyrics || "暂无歌词";  // 默认显示歌词
    }
    // 更新音频时长和进度条
    main.ondurationchange = function () {
        audioTime.innerText = transTime(main.duration);
        main.currentTime = 0;
        updateProgress();
    };
}
//歌词
let lyrics = [];
// 解析歌词
const parseLyrics = (lyricsText) => {
  const lines = lyricsText.split('\n');
  const lyrics = [];
  const metadata = []; // 存储作词、作曲等信息
  const regex = /^\[([0-9]{2}):([0-9]{2})\.(\d{2,3})\](.*)$/;
  const metaRegex = /^(作词|作曲|编曲|演唱|制作|歌手|专辑|编制)/;

  lines.forEach((line, index) => {
    line = line.trim().replace(/\ufeff/g, ''); // 去除 BOM 头

    if (!line) return; // 跳过空行

    // 处理作词、作曲、编曲等信息，并存入 metadata
    if (metaRegex.test(line)) {
      metadata.push({ time: 0, text: line });
      return;
    }

    const match = line.match(regex);
    if (match) {
      const minutes = parseInt(match[1]);
      const seconds = parseInt(match[2]);
      const milliseconds = parseInt(match[3]);
      const text = match[4].trim();

      if (text) {
        const time = minutes * 60 + seconds + milliseconds / 1000;
        lyrics.push({ time, text });
      }
    } else {
      console.warn(`歌词解析失败: 第 ${index + 1} 行： ${line}`);
    }
  });

  // 如果没有有效歌词，返回“没有歌词”
  return lyrics.length > 0 ? [...metadata, ...lyrics] : [{ time: 0, text: '没有歌词' }];
};
// 更新歌词
let currentLyricIndex = -1;  // 当前歌词索引
const updateLyrics = () => {
    if (!main) return;

    const currentTime = main.currentTime;  // 获取当前播放的时间

    // 遍历歌词数组，找出当前播放时间对应的歌词
    for (let i = 0; i < lyrics.length; i++) {
        if (currentTime >= lyrics[i].time && currentLyricIndex !== i) {
            currentLyricIndex = i;
            displayLyrics(); // 显示当前歌词
        }
    }
};
const displayLyrics = () => {
    if (currentLyricIndex >= 0 && currentLyricIndex < lyrics.length) {
        const lyricsContainer = document.getElementById("lyrics-container");
        if (lyricsContainer) {
            let linesToDisplay = "";
            for (let i = currentLyricIndex; i < currentLyricIndex + 5; i++) {
                if (lyrics[i]) {
                    linesToDisplay += `<p>${lyrics[i].text}</p>`;
                }
            }
            lyricsContainer.innerHTML = linesToDisplay;
        }
    }
};
setInterval(() => {
    displayLyrics();
    currentLyricIndex++;
    if (currentLyricIndex >= lyrics.length) {
        currentLyricIndex = 0;  // 循环播放歌词
    }
}, 1000); // 每秒更新一次歌词
// 每次音频播放时更新歌词
main.addEventListener('timeupdate', updateLyrics);
// 初始化并播放歌曲
function initAndPlay(music) {
    initMusic(music);  // 初始化音乐信息
    pause.classList.remove('icon-play');
    pause.classList.add('icon-pause');
    main.play();  // 播放音乐
    rotateRecord();  // 播放时旋转唱片
}
// 调用搜索
searchBtn.addEventListener('click', function() {
    var query = searchInput.value.trim();
    var selectedApi = apiSelect.value;

    if (query) {
        if (selectedApi) {
            searchMusic(query, selectedApi);  // 进行音乐搜索
        } else {
            alert('Please select a music source!');
        }
    } else {
        alert('Please enter a search term!');
    }
});
// 倍速功能（这里直接暴力解决了）
speed.addEventListener('click', function (event) {
    var speedText = speed.innerText;
    if (speedText == "1.0X") {
        speed.innerText = "1.5X";
        main.playbackRate = 1.5;
    }
    else if (speedText == "1.5X") {
        speed.innerText = "2.0X";
        main.playbackRate = 2.0;
    }
    else if (speedText == "2.0X") {
        speed.innerText = "0.5X";
        main.playbackRate = 0.5;
    }
    else if (speedText == "0.5X") {
        speed.innerText = "1.0X";
        main.playbackRate = 1.0;
    }
});
// 使唱片旋转
function rotateRecord() {
    recordImg.classList.add('rotate');  // 添加旋转动画
}
// 停止唱片旋转
function rotateRecordStop() {
    recordImg.classList.remove('rotate');  // 移除旋转动画
}
// 存储上一次的音量
var lastVolumn = 100
// 滑块调节音量
main.addEventListener('timeupdate', updateVolumn);
function updateVolumn() {
    main.volume = volumeTogger.value / 100;
}
// 点击音量调节设置静音
volume.addEventListener('click', setNoVolumn);
function setNoVolumn() {
    if (volumeTogger.value === 0) {
        if (lastVolumn === 0) {
            lastVolumn = 100;
        }
        volumeTogger.value = lastVolumn;
        volume.style.backgroundImage = "url('img/音量.png')";
    }
    else {
        lastVolumn = volumeTogger.value;
        volumeTogger.value = 0;
        volume.style.backgroundImage = "url('img/静音.png')";
    }
}
// 播放模式切换（单曲循环、顺序播放、随机播放）
var modeId = 1;  // 默认模式为顺序播放
mode.addEventListener('click', function (event) {
    modeId = modeId + 1;
    if (modeId > 3) {
        modeId = 1;  // 重置为单曲循环
    }
    mode.style.backgroundImage = "url('img/mode" + modeId.toString() + ".png')";
});
// 播放结束时，根据模式选择下一首
main.onended = function () {
    //单曲循环
    if (modeId === 2) {
        main.currentTime = 0;
        main.play();
    } else if (modeId === 1) {
        // 顺序播放：跳到下一首
        musicId = (musicId + 1) % musicListData.length;
        initAndPlay(musicListData[musicId]);
    } else if (modeId === 3) {
        // 随机播放：随机选择下一首
        let randomId;
        do {
            randomId = Math.floor(Math.random() * musicListData.length);
        } while (randomId === musicId); // 防止随机选中当前正在播放的歌曲
        musicId = randomId;
        initAndPlay(musicListData[musicId]);
    }
};
// 进入全屏
const fullscreenButton = document.getElementById('fullscreen-btn');
// 判断是否支持全屏
function enterFullscreen() {
    const elem = document.documentElement; // 获取 HTML 元素

    if (elem.requestFullscreen) {
        elem.requestFullscreen();
    } else if (elem.mozRequestFullScreen) { // Firefox
        elem.mozRequestFullScreen();
    } else if (elem.webkitRequestFullscreen) { // Chrome, Safari and Opera
        elem.webkitRequestFullscreen();
    } else if (elem.msRequestFullscreen) { // IE/Edge
        elem.msRequestFullscreen();
    }
}
function exitFullscreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.mozCancelFullScreen) { // Firefox
        document.mozCancelFullScreen();
    } else if (document.webkitExitFullscreen) { // Chrome, Safari and Opera
        document.webkitExitFullscreen();
    } else if (document.msExitFullscreen) { // IE/Edge
        document.msExitFullscreen();
    }
}
// 切换全屏
fullscreenButton.addEventListener('click', function() {
    if (!document.fullscreenElement) {
        enterFullscreen();
        fullscreenButton.innerHTML = '<i class="fa-solid fa-compress"></i> 退出';
    } else {
        exitFullscreen();
        fullscreenButton.innerHTML = '<i class="fa-solid fa-expand"></i> 全屏';
    }
});
function adjustScale() {
    const container = document.getElementById('container');
    const designWidth = 1280;
    const designHeight = 720;
    // 获取屏幕尺寸
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;
    // 计算缩放比例
    const scaleX = screenWidth / designWidth;
    const scaleY = screenHeight / designHeight;
    const scale = Math.min(scaleX, scaleY);
    // 应用缩放
    container.style.transform = `translate(-50%, -50%) scale(${scale})`;
}
// 初始化执行
adjustScale();
// 窗口变化时重新调整
window.addEventListener('resize', adjustScale);
window.addEventListener('orientationchange', adjustScale);