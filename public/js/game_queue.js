define(['mediator'], function (mediator) {
    
    function set_queue_window(element){
        q = $(element);
        row_template = q.find("#row_template").text();
    }

    function add_game(data){
        row = _.template(row_template)(data);
        q.find('tbody').append(row);
    }

    function remove_game(data){

    }

    return {
        set_queue_window: set_queue_window,
        add_game: add_game,
        remove_game: remove_game
    };
});