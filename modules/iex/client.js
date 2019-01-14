
const SocketClient = require('socket.io-client')

const url = 'http://localhost:9009'


const socket = SocketClient(url)

socket.on('message', (data)=> {
    console.log(data)
 })

 socket.on('connect', () => {
     console.log("Connection created")
 })
