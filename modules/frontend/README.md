## Frontend
This is the frontend application which contains the dashboard. This single page application does not receive any inputs from the user and simply displays the data that is stored in the backend similarly to the MVP architecture.

The frontend consists of mainly two components: Status Feed (Tweets) and Stock Status (Graph). All of the data is received from the backend. The frontend should continuously query the backend via `POST` to received the updates in a fixed interval such as "every second". The response to this query will include the data of all of the tweets to display, as well as all the stock data to display on the graph.

There will be two main endpoints to use:

**Primary Serve: [GET]**
```
/
```

**Receive Updates: [POST]**
```
/getData
``` 

<img width="804" alt="screen shot 2019-01-11 at 15 23 54" src="https://user-images.githubusercontent.com/17438617/51036147-e44c1a00-15b4-11e9-84ba-a9767bdb458b.png">
