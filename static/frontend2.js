var me = {};
me.avatar = "/static/logo.png";

var you = {};
you.avatar = "/static/women.png";

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}

//-- No use time. It is a javaScript effect.
function insertChat(who, text, time){
    if (time === undefined){
        time = 0;
    }
    var control = "";
    var date = formatAMPM(new Date());

    if (who == "me"){
        control = '<li style="width:100%">' +
                        '<div class="msj macro">' +
                        '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ me.avatar +'" /></div>' +
                            '<div class="text text-l">' +
                                '<p>'+ text +'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '</div>' +
                    '</li>';
    }else{
        control = '<li style="width:100%;">' +
                        '<div class="msj-rta macro">' +
                            '<div class="text text-r">' +
                                '<p>'+text+'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '<div class="avatar" style="padding:0px 0px 0px 10px !important"><img class="img-circle" style="width:100%;" src="'+you.avatar+'" /></div>' +
                  '</li>';
    }
    setTimeout(
        function(){
            $(document).ready(function(){
                $("ul").append(control).scrollTop($("ul").prop('scrollHeight'));
            });
        }, time);

}

function resetChat(){
    $("ul").empty();
}

$(document).ready(function(){
    $("#mytext").on("keydown", function(e){
        if (e.which == 13){
            var text = $(this).val();
            if (text !== ""){
                insertChat("you", text);
                const Url = 'http://127.0.0.1:4567/summary?company=' + text ;
                $.ajax({
                    url: Url,
                    type: "GET",
                    success: function(result){
                        insertChat("me", result);
                    },
                    error:function(error){
                        console.log('Error ${error}')
                    }
                })
                $(this).val('');
            }
        }
    });
});

// $(document).ready(function(){
//     $("#mytext").on("keydown", function(e){
//         if (e.which == 13){
//             var text = $(this).val();
//             if (text !== ""){
//                 insertChat("you", text);
//                 const Url = Url = 'http://127.0.0.1::4567/summary?company=' + text.split(" ")[1] ;;
//                 // if(text.split(" ")[0]=='summarize'){
//                 //     Url = 'http://127.0.0.1::4567/summary?company=' + text.split(" ")[1] ;
//                 // }
//                 // else {
//                 //     Url = 'https://127.0.0.1/plm'
//                 // }
//                 $.ajax({
//                     url: Url,
//                     type: "GET",
//                     success: function(result){
//                         insertChat("me", result);
//                     },
//                     error:function(error){
//                         console.log('Error ${error}')
//                     }
//                 })
//                 $(this).val('');
//             }
//         }
//     });
// });


$('body > div > div > div:nth-child(2) > span').click(function(){
    $(".mytext").trigger({type: 'keydown', which: 13, keyCode: 13});
})

//-- Clear Chat
// resetChat();

function myFunction() {
  var test  = document.getElementById("mytext");
  console.log(test);
}
//-- Print Messages
// insertChat("me", "Hello Tom...", 0);
// document.getElementById("mytext").onclick = function() {myFunction()};
// insertChat("you", "Hi, Pablo", 1500);
// insertChat("me", "What would you like to talk about today?", 3500);
// insertChat("you", "Tell me a joke",7000);
// insertChat("me", "Spaceman: Computer! Computer! Do we bring battery?!", 9500);
// insertChat("you", "LOL", 12000);


//-- NOTE: No use time on insertChat.
