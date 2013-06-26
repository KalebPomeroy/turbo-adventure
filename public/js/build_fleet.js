$(function(){
    require(['mediator'],function(mediator){

        $(".add_ship").click(function(){
            mediator.publish('hq.add_ship', {'ship': $(this).attr('data-ship')})
            return false;
        });

        mediator.subscribe('hq.ship_added', function(ship){
            $("#fleet").append("<p>" + ship.name + "</p>")
        })
    });    
    $('a').popover({placement:'right', container: 'body', trigger: 'hover'});
});