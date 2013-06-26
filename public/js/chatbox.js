define(['mediator', 'lib/moment'], function (mediator) {
    var c = undefined; 

    function set_chat_window(element){
        c = $(element)
    }

    function connect_message(data){
        mediator.publish("chat.add_message", {'message': "Connecting to server..."})
    };

    function add_to_chat_box(data){ 

        time = moment().format('h:mm:ss');
        message = "[" + time + "] " + data.message

        if(data.message_type=="self_chat"){
            $(c).append("<div class='alert alert-success'>" + message + "</div>");
        } else if(data.message_type=="another_player_chat"){
            $(c).append("<div class='alert alert-info'>" + message + "</div>");
        } else {
            $(c).append("<div class='alert'>" + message + "</div>");
        }
    }

    return {
        set_chat_window: set_chat_window,
        add_message: add_to_chat_box,
        connect_message: connect_message
    };
});