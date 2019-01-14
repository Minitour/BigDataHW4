const express = require('express')
const spawn = require('threads').spawn;
const path = require('path')

const app = express()
app.use(express.json())
const port = 5423

const symbols = ['GE','MSFT','APPL','AIG','MLNX','INTC','QCOM','PS','SIE']

var data = {
    tweets : [],
    stocks : {}
}

function generateText(length) {
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  
    for (var i = 0; i < length; i++)
      text += possible.charAt(Math.floor(Math.random() * possible.length));
  
    return text;
  }
  

spawn( async (input, done) => {
    const sleep = (waitTimeInMs) => new Promise(resolve => setTimeout(resolve, waitTimeInMs));
    while (true) {
        // sleep for 1 second
        await sleep(1000);
        // call done
        done({});
    }
})
.send({})
.on('message', (response)=> {
    // add random data to data
    data.tweets.push(generateTweet())
    
    var stock_value = generateStock()
    
    var companyKey = symbols[Math.floor(Math.random()*symbols.length)]

    if (data.stocks[companyKey] != undefined) {
        data.stocks[companyKey].stockPrices.push(stock_value)
    }else {
      data.stocks[companyKey] = {
        "stockPrices" : [
          stock_value
        ]
      }
    }
})

app.post('/getData',(req,res)=>{
    res.send(data);
})

app.listen(port);
console.log('Server now listening on port '  + port);

app.get("/", (req, res)=> {
  res.sendFile(path.join(__dirname + "/../index.html"))
})


function generateTweet() {
    var template = {
      "tweet_id" : "234234234234434",
      "positive" : false
    }

    return template;
}

function generateStock() {
  return { "value": Math.random() * 1000, "timestamp" : new Date().getTime() }
}