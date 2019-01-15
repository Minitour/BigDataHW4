//var socket = require('socket.io-client')('ws://localhost:9009');
//socket.on('connect', function(){
//    console.log("connect")
//});
//socket.on('event', function(data){
//    console.log(data)
//});
//socket.on('disconnect', function(){
//    console.log("disconnect")
//});

var net = require('net');

var client = new net.Socket();

client.connect(3001, '127.0.0.1', function() {
	console.log('Connected');
});

client.on('data', function(data) {
	console.log('Received: ' + data);
});

client.on('close', function() {
	console.log('Connection closed');
});

