$(function(){

    //
    // Set up the chat system
    // 
    require(['chatbox', 'mediator'],function(chatbox, mediator){

        chatbox.set_chat_window($("#chatbox"))

        mediator.subscribe('event.connect', chatbox.connect_message);
        mediator.subscribe('chat.add_message', chatbox.add_message);


        mediator.publish("chat.add_message", {'message': "Welcome to chat."})
        mediator.publish('event.connect');


        $("#say_form").submit(function(){
            mediator.publish('chat.say', {'message': $("#chat").val()})
            $("#chat").val("")
            return false;
        });
    });    

    //
    // Set up the chat system
    // 
    require(['game_queue', 'mediator'],function(q, mediator){

        q.set_queue_window($("#queue"))

        mediator.subscribe('queue.add_game', q.add_game);
        mediator.subscribe('queue.remove_game', q.remove_game);

        mediator.publish("queue.list_games")

    });

});    

