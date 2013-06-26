define(['mediator'], function (mediator) {
    var fleet_id = undefined; 

    function set_id(id){
        fleet_id = id;
    }

    function update_fleet(fleet){
        console.log(fleet);

        // Actually update it in the UI
    }

    function add_ship(ship){
        mediator.publish('hq.fleet.add_ship', {'fleet_id': fleet_id, 'ship': ship})
    };


    return {
        set_id: set_id,
        add_ship: add_ship,
        update: update_fleet,
    };
});