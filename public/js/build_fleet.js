$(function(){
    require(['mediator', 'fleet'],function(mediator, fleet){

        fleet.set_id($("#fleet_id").val());

        $(".add_ship").click(function(){
            modal = $("#" + $(this).attr('data-target'));

            ship = modal.find('[name=ship]').val()
            primary = modal.find('[name=Primary]').val();
            secondary = modal.find('[name=Secondary]').val();
            tertiary = modal.find('[name=Tertiary]').val();
            

            // // TODO: Figure out why these don't work
            // modal.find('[name=Primary]').val("None");
            // modal.find('[name=Secondary]').val("None");
            // modal.find('[name=Tertiary]').val("None");
            
            fleet.add_ship({
                'type': ship,
                'primary': primary,
                'secondary': secondary,
                'tertiary': tertiary
            });    
            // fleet.show_add_ship_modal()
            modal.modal('hide')
            return false;
        });


        mediator.subscribe('hq.fleet.update', fleet.update)
        fleet.get()

        


    });    
    $('a').popover({placement:'right', container: 'body', trigger: 'hover'});
    $('.selectpicker').selectpicker();
});
