console.log("I'm in a main....");

$(function(){

    require(['chatbox', 'mediator'],function(chatbox, mediator){

        mediator.subscribe('event.connect', chatbox.connect_message);
        mediator.subscribe('chat.add_message', chatbox.add_to_chat_box);


        mediator.publish("chat.add_message", {'message': "Welcome to chat."})
        mediator.publish('event.connect', {'username': 'kaleb'});


        $("#submit_button").click(function(){
            mediator.publish('chat.say', {'message': $("#chat").val()})
        });
    })
});    

