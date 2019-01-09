const SocketClient = require('socket.io-client')
const express = require('express')
const app = express()
const port = 3000

const WINDOW_SIZE = 3600000 // 1 hour in millisconds

// create socket object
const url = 'https://ws-api.iextrading.com/1.0/tops'

const socket = SocketClient(url)

/**
 * This is a js object which contains the current subscribed symbols and their expiration date.
 */
var symbol_queue = {}

socket.on('message', (data)=> { consume(data) })

socket.on('connect', () => {
    console.log("Connection created")
    init_application()
})


/**
 * This function sets up all the express routes.
 * 
 * We do this in a function and not in a global scope so we can init the app only after the socket connection was established.
 */
function init_application() {
    app.post('/api/subscribe', function(req, res) {
        var symbol = req.body.symbol;
    });
}

// set up routes


/**
 * This function consumes a single data item received from the stream.
 * 
 * @param {*} item 
 */
function consume(item) {

}

/**
 * Adds a new symbol to the queue.
 * 
 * @param {String} symbol 
 */
function addToQueue(symbol) {
    symbol_queue[symbol] = new Date().getTime() + WINDOW_SIZE;
}

/**
 * Checks if the symbol in the queue exists and has a valid timestamp.
 * 
 * @param {String} symbol 
 */
function doesExistInQueue(symbol) {
    var timeStamp = symbol_queue[symbol]
    
    if (timeStamp == undefined) {
        // time stamp not found
        return false
    } else {
        // check expiration time
        if (timeStamp > new Date().getTime()){
            return true
        } else {
            delete symbol_queue[symbol]
            return false
        }
    }
}
