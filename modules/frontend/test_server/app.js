const express = require('express')
const spawn = require('threads').spawn;

const app = express()
app.use(express.json())
const port = 5423

var data = {
    tweets : [],
    stocks : []
}

spawn( (input, done) => {

    // while true

    // sleep for 1 second

    // call done
})
.on('message', (response)=> {
    // add random data to data
})

app.post('/getData',(req,res)=>{
    res.send(data);
})

app.listen(port);