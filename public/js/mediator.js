define(["./socketio",], function(socketio){

    var socket = socketio.socket;
    var channels = {};

    var subscribe = function(channel, fn){
        if (! channels[channel]){
            channels[channel] = [];
        }
        channels[channel].push({ context: this, callback: fn });
        socket.on(channel, function(data) { publish(channel, data); });
        return this;
    };
 
    publish = function(channel){

        var args = Array.prototype.slice.call(arguments, 1);

        socket.emit(channel, {"data": args});
        
        if (!channels[channel]){
            return false;
        }

        for (var i = 0, l = channels[channel].length; i < l; i++) {
            var subscription = channels[channel][i];
            subscription.callback.apply(subscription.context, args);
        }

        return this;
    };
 
    return {
        channels: {},
        publish: publish,
        subscribe: subscribe,
        installTo: function(obj){
            obj.subscribe = subscribe;
            obj.publish = publish;
        }
    };
 
});