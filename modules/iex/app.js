const server = require('http').createServer();
const io = require('socket.io')(server);
const spawn = require('threads').spawn;
const express = require('express')
const app = express()
app.use(express.json())
const port = 3000
const WINDOW_SIZE = 3600000 // 1 hour in millisconds

 io.listen(port + 1);
 console.log('Stream Avaiable on port '  + (port + 1))

/**
 * This is a js object which contains the current subscribed symbols and their expiration date.
 */
var queue = {}

/**
 * Primary background task
 */
const thread = spawn(function(input, done) {

    const url = 'https://ws-api.iextrading.com/1.0/tops'

    const SocketClient = require('socket.io-client')

    const socket = SocketClient(url)
    
    socket.on('message', (data)=> {
        let objc = JSON.parse(data)
        done(objc); 
     })
    
     socket.on('connect', () => {
         console.log("Sucessfully Connected to IEX")
         socket.emit('subscribe','firehose')
     })
});

thread
.send({})
.on('message', (response)=> {
    // apply transformations if needed
    console.log(response.symbol)

    if (response == undefined) {
        return;
    }

    if (!('symbol' in response)) {
        return;
    }

    updateQueueIfNeededFor(response.symbol);

    // if stock symbo is in queue then consume it
    if (existsInQueue(response.symbol)){
        consume(response);
    }
})

/**
 * Check if symbol is in our queue (sub box)
 * @param {String} symbol 
 */
function existsInQueue(symbol) {
    return symbol.toLowerCase() in queue;
}

/**
 * check if the symbol is in the queue and if it has expired or not
 * @param {String} symbol 
 */
function updateQueueIfNeededFor(symbol) {
    var timestamp = queue[symbol];

    if (timestamp != undefined) {
        if (timestamp < new Date().getTime()) {
            // timestamp expired
            delete queue[symbol];
        }
    }
}

/**
 * an object which contains the data to send down the stream.
 * @param {Object} data 
 */
function consume(data) {
    io.sockets.emit('message', data);
}

app.post('/api/subscribe',(req,res)=>{
    // subscribe
    var symbol = req.body.symbol;

    if (symbol == undefined) {
        res.send({code : 400 })
        return
    }

    symbol = symbol.toLowerCase();

    // add symbol to queue with current time + window size aka expiration date.
    queue[symbol] = new Date().getTime() + WINDOW_SIZE;
    
    // response success
    res.send({ code : 200})
})

app.listen(port);