window.onload = function () {
    var minSize = 10;
    var maxSize = 40;
    var newOne = 500;
    var flakColor = "#f5f5f5fa";
    var flak = $("<div></div>").css({
        position: "absolute",
        "top": "0px"
    }).html("✽");
    var dhight = $(window).height();
    var dw = $(window).width() - 80;

    setInterval(function () {
        var sizeflak = minSize + Math.random() * maxSize;
        var startLeft = Math.random() * dw;
        var startOpacity = 0.7 + Math.random() * 0.3;
        var endTop = dhight - 100;
        var endLeft = Math.random() * dw;
        var durationfull = 5000 + Math.random() * 3000;
        flak.clone().appendTo($("body")).css({
            "left": startLeft,
            "opacity": startOpacity,
            "font-size": sizeflak,
            "color": flakColor
        }).animate({
            "top": endTop,
            "left": endLeft,
            "opacity": 0.1
        }, durationfull, function () {
            $(this).remove();
        });
    }, newOne);
};