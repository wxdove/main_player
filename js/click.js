jQuery(document).ready(function($) {
    var a_idx = 0;
    var messages = ["❤不做咸鱼！❤", "❤拒绝懒惰！❤", "❤你好呀！❤", "❤欢迎！❤", "❤热烈欢迎！❤", "❤想做吃货❤", "❤小汪加油❤", "❤早睡早起❤", "❤向大佬学习❤", "❤扶我起来~❤", "❤come on❤", "❤一直在路上~❤", "❤累了~❤", "❤再趴一会❤", "❤66666❤", "❤高兴的飞起*****❤"];
;

    $("body").click(function(e) {
        var message = messages[Math.floor(Math.random() * messages.length)];
        var $i = $("<span></span>").text(message);
        var x = e.pageX,
            y = e.pageY;
        $i.css({
            "z-index": 999999,
            "top": y - 20,
            "left": x,
            "position": "absolute",
            "font-weight": "bold",
            "font-size": "18px",
            "opacity": 1,
            "color": getRandomBrightColor()
        });
        $i.html($i.html().replace(/❤/g, "<span style='color: red;'>❤</span>"));
        $("body").append($i);
        $i.animate({
            "top": y - 180,
            "opacity": 0
        }, 1500, function() {
            $i.remove();
        });
    });
    function getRandomBrightColor() {
        var r = ~~(180 + Math.random() * 75);
        var g = ~~(180 + Math.random() * 75);
        var b = ~~(180 + Math.random() * 75);
        return "rgb(" + r + "," + g + "," + b + ")";
    }
});
