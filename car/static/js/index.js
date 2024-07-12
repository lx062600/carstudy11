<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

$(document).ready(function(){
    $('.icon1').hover(
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon1-2.png" %}")');
        },
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon1.png" %}")');
        }
    );
    $('.icon2').hover(
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon2-2.png" %}")');
        },
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon2.png" %}")');
        }
    );
    $('.icon3').hover(
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon3-2.png" %}")');
        },
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon3.png" %}")');
        }
    );
    $('.icon4').hover(
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon4-2.png" %}")');
        },
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon4.png" %}")');
        }
    );
    $('.icon5').hover(
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon5-2.png" %}")');
        },
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon5.png" %}")');
        }
    );
    $('.icon6').hover(
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon6-2.png" %}")');
        },
        function() {
            $(this).find('.icon-bg').css('background-image', 'url("{% static "images/icon6.png" %}")');
        }
    );

    // 为其他图标元素重复上述hover事件处理函数...
});