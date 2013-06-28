define(['mediator'], function (mediator) {
    var fleet_id = undefined; 

    function set_id(id){
        fleet_id = id;
    }

    function update_fleet(fleet){
        $("#fleet").html(JSON.stringify(fleet, undefined, 2));
        // Actually update it in the UI
    }

    function add_ship(ship){
        mediator.publish('hq.fleet.add_ship', {'fleet_id': fleet_id, 'ship': ship})
    };

    function get(){
        mediator.publish('hq.fleet.get', {'fleet_id': fleet_id})
    }

    return {
        get: get,
        set_id: set_id,
        add_ship: add_ship,
        update: update_fleet,
    };
});