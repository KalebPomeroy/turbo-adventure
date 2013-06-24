define(['mediator'], function (mediator) {
    var c =  $("#chatbox"); 

    function connect_message(data){
        mediator.publish("chat.add_message", {'message': "Connecting to server..."})
    };

    function add_to_chat_box(data){ 
        $(c).append("<p class='alert alert-info'>" + data.message + "</p>")
    }

    return {
        add_to_chat_box: add_to_chat_box,
        connect_message: connect_message
    };
});