define(['mediator'], function (mediator) {
    var c =  $("#chatbox"); 

    function connect_message(data){
        mediator.publish("chat.add_message", {'message': "Connecting to server..."})
    };

    function add_to_chat_box(data){ 
        $(c).append(data.message + "<br />")
    }

    return {
        add_to_chat_box: add_to_chat_box,
        connect_message: connect_message
    };
});