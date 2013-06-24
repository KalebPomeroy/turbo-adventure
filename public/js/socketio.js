define(function(){
    var socket
    , protocol = "http://"
    , location = window.location.hostname
    , port = 8000

    socket = new io.connect(protocol + location + ":" + port + "?user=kaleb", {
        rememberTransport: false
    });

    return {
        socket: socket 
    };
});