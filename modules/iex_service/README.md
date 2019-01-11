## IEX Service 
The IEX Service, is the module in this project which is in charge of receiving the stocks data from IEX API in real time, process it and then forward it onto another stream.

This service contains two servers. One server that is socket based, which acts as our stream pipeline, while the second server is an `HTTP Server` which handles few `POST` requests to manage and manipulate the output of the stream. Both servers run in parallel on different threads. 


## Setup

### Client 

Setup a client which listens to the stream. This will be done by the Spark Service, but for simplicity we'll stick to NodeJS 

```javascript
const SocketClient = require('socket.io-client')

// localhost:3001 is the IEX service stream.
const url = 'http://localhost:3001' 

const socket = SocketClient(url)
    
socket.on('message', (data)=> {
    // handle data
    console.log(data)
 })

 socket.on('connect', () => {
     console.log("Connection created")
 })
```

### Subscribe to Topic
Unlike other streaming applications, In order to modify the stream we make a `POST` request to `/api/subscribe` to let the IEX service know which stocks do we want to listen to.

For example, let's assume we want to listen to the stocks of `AIG`. A request might look like this in python:

```python
import requests

url = "http://localhost:3000/api/subscribe"

payload = '{"symbol":"AIG"}'

response = requests.request("POST", url, data=payload)

print(response.text)
```

After making this request, you should receive the following response:
```json
{ "code" : 200 }
```
Which indicates that the IEX service will now emit events with the symbol that was specified.

The IEX service will retain the symbol in its queue for one hour from its initial request. If another `POST` request is made with a symbol already existing in the queue then its lease time will be renewed to another hour.


