$(function(){
    require(['mediator', 'fleet'],function(mediator, fleet){

        fleet.set_id($("#fleet_id").val())

        $(".add_ship").click(function(){
            fleet.add_ship($(this).attr('data-ship'))
            return false;
        });

        mediator.subscribe('hq.fleet.update', fleet.update)
        fleet.get()

    });    
    $('a').popover({placement:'right', container: 'body', trigger: 'hover'});
});