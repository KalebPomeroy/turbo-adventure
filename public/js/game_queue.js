define(['mediator'], function (mediator) {
    
    function set_queue_window(element){
        q = $(element);
        row_template = q.find("#row_template").text();
    }

    function list_games(data){
        _.each(data, function(d){
            console.log(d);
            row = _.template(row_template)({game: d});
            q.find('tbody').append(row);
        });
    }

    function remove_game(){
        // This is the UI piece when a game should be removed
    }

    return {
        set_queue_window: set_queue_window,
        list_games: list_games,
        remove_game: remove_game
    };
});