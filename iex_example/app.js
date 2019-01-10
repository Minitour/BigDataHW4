const server = require('http').createServer();
const io = require('socket.io')(server);
const spawn = require('threads').spawn;
const express = require('express')
const app = express()
app.use(express.json())
const port = 3000

const WINDOW_SIZE = 3600000 // 1 hour in millisconds

/**
 * This is a js object which contains the current subscribed symbols and their expiration date.
 */
var symbol_queue = {}


 io.listen(port + 1);

// create socket object

var arr = []

const thread = spawn(function(input, done) {

    const url = 'https://ws-api.iextrading.com/1.0/tops'

    const SocketClient = require('socket.io-client')

    const socket = SocketClient(url)
    
    socket.on('message', (data)=> {
        let objc = JSON.parse(data)
        done(objc); 
     })
    
     socket.on('connect', () => {
         console.log("Connection created")
         socket.emit('subscribe','firehose')
     })
});

thread
.send({})
.on('message', (response)=> {
    // TODO: manipulate the response and boradcast it
    io.sockets.emit('message', response);
})

app.post('/api/subscribe',(req,res)=>{
    // subscribe

    // response success
    res.send({ code : 200, result: arr })
})

app.listen(port);