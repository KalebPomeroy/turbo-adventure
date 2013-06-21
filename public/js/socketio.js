define(function(){
    var socket
    , protocol = "http://"
    , location = window.location.hostname
    , port = 8000

    socket = new io.connect(protocol + location + ":" + port, {
        rememberTransport: false
    });

    return {
        socket: socket 
    };
});