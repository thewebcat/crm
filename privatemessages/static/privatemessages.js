function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function setCookie(key, value) {
    document.cookie = escape(key) + '=' + escape(value);
}

function getNumEnding(iNumber, aEndings) {
    var sEnding, i;
    iNumber = iNumber % 100;
    if (iNumber>=11 && iNumber<=19) {
        sEnding=aEndings[2];
    }
    else {
        i = iNumber % 10;
        switch (i)
        {
            case (1): sEnding = aEndings[0]; break;
            case (2):
            case (3):
            case (4): sEnding = aEndings[1]; break;
            default: sEnding = aEndings[2];
        }
    }
    return sEnding;
}

var timezone = getCookie('timezone');

if (timezone == null) {
    setCookie("timezone", jstz.determine().name());
}

function activate_chat(thread_id, user_name, number_of_messages) {
    $("div.chat form.message_form div.compose textarea").focus();

    function scroll_chat_window() {
        $("div.chat div.conversation").scrollTop($("div.chat div.conversation")[0].scrollHeight);
    }

    function soundClick() {
        var audio = new Audio(); // Создаём новый элемент Audio
        audio.src = '/static/bb2.mp3'; // Указываем путь к звуку "клика"
        audio.autoplay = true; // Автоматически запускаем
    }

    scroll_chat_window();

    //var ws;
    var conn

    function start_chat_ws() {
        var transports = [
                     'websocket',
                     'xdr-streaming',
                     'xhr-streaming',
                     'iframe-eventsource',
                     'iframe-htmlfile',
                     'xdr-polling',
                     'xhr-polling',
                     'iframe-xhr-polling',
                     'jsonp-polling'
                    ]
        conn = new SockJS('http://crm.fxbox.org/chat', transports);
        console.log('Connecting...');
        conn.onopen = function() {
            console.log('Connected.');
            conn.send('{"type":"auth","thread_id":"'+thread_id+'"}');
        };
        conn.onmessage = function(event) {
            var message_data = JSON.parse(event.data);
            console.log(message_data);
            if (message_data.name == "message") {
                $('._im_typing_name').fadeOut();
                var date = new Date(message_data.timestamp*1000);
                var time = $.map([date.getHours(), date.getMinutes(), date.getSeconds()], function(val, i) {
                    return (val < 10) ? '0' + val : val;
                });
                $("div.chat div.conversation div.im-messages").append('<div class="message"><p class="author ' + ((message_data.sender == user_name) ? 'we' : 'partner') + '"><span class="datetime">' + time[0] + ':' + time[1] + ':' + time[2] + '</span> ' + message_data.sender + ':</p><p class="message">' + message_data.text.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/\n/g, '<br />') + '</p></div>');
                scroll_chat_window();
                number_of_messages["total"]++;
                if (message_data.sender == user_name) {
                    number_of_messages["sent"]++;
                } else {
                    number_of_messages["received"]++;
                    soundClick();
                }
                $("div.chat p.messages").html('<span class="total">' + number_of_messages["total"] + '</span> ' + getNumEnding(number_of_messages["total"], ["сообщение", "сообщения", "сообщений"]) + ' (<span class="received">' + number_of_messages["received"] + '</span> получено, <span class="sent">' + number_of_messages["sent"] + '</span> отправлено)');
                if (true) {}
            }
            if (message_data.name == "typing") {
                if (message_data.sender != user_name) {
                    if (message_data.typing) {
                        console.log("Печтатает...");
                        $('._im_typing_name').text('Печтатает...');
                        $('._im_typing_name').fadeIn();
                        scroll_chat_window();
                    } else {
                        console.log("Закончил печатать...");
                        //$('._im_typing_name').text('Закончил печатать...');
                        setTimeout(function() {
                            $('._im_typing_name').fadeOut();
                            scroll_chat_window();
                        },400);
                    }
                }
            }
            
        }
        conn.onclose = function(){
            // Try to reconnect in 5 seconds
            console.log('Reconnecting...');
            setTimeout(function() {start_chat_ws()}, 5000);
        };
    }

    start_chat_ws();

    function send_message() {
        var textarea = $("textarea#message_textarea");
        if (textarea.val() == "") {
            return false;
        }
        if (conn.readyState != SockJS.OPEN) {
            return false;
        }
        conn.send('{"type":"message","message":"'+textarea.val()+'"}');
        textarea.val("");
    }

    $("form.message_form div.send button").click(send_message);

    $("textarea#message_textarea").keydown(function (e) {
        // Ctrl + Enter
        if (e.ctrlKey && e.keyCode == 13) {
            send_message();
        }
    });

    var timeout;
    var printing = 0;

    $("textarea#message_textarea").on('keyup',function(e){
        if (!(e.ctrlKey && e.keyCode == 13) && !(!e.ctrlKey && e.keyCode == 17)) {
            printing = printing + 1;

            // Вызываем, только если изменилось значение
            if (printing == 1) {
                setTimeout(function() {
                    //console.log("Начал ввод...")
                    conn.send('{"type":"typing","typing":"1"}');
                },300);
            }

            if (printing != 0) {
                // Делаем задержку и обнуляем предыдущую
                if(timeout) { clearTimeout(timeout); }
                // Новый таймаут
                timeout = setTimeout(function() {
                    // Выполняем поиск
                    //console.log("Закончил ввод...")
                    conn.send('{"type":"typing","typing":"0"}');
                    printing = 0;
                },2000);
            }
        }
    });
}
