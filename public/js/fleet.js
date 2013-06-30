define(['mediator'], function (mediator) {
    var fleet_id = undefined; 

    function set_id(id){
        fleet_id = id;
    }

    function change_name(new_name){

        mediator.publish('hq.fleet.change_name', {'fleet_id': fleet_id, 'name': new_name});
    }

    function update_fleet(fleet){

        template_string = $("#fleet-template").html();
        t = _.template(template_string);
        $("#fleet").html(t(fleet));

        // TODO: This logic needs to be elsewhere
        $("#fleet_name").blur(function(){
            change_name($("#fleet_name").val());
        });
        $(".decom").click(function(){
            ship = $(this).attr('data-ship');
            mediator.publish('hq.fleet.remove_ship', {'fleet_id': fleet_id, 'ship': ship});
        });
    }

    function add_ship(ship){
        console.log(ship);
        mediator.publish('hq.fleet.add_ship', {'fleet_id': fleet_id, 'ship': ship});
    };

    function get(){
        mediator.publish('hq.fleet.get', {'fleet_id': fleet_id});
    }

    return {
        get: get,
        set_id: set_id,
        add_ship: add_ship,
        update: update_fleet,
    };
});