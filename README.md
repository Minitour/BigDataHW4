# TweeStock
We'll monitor the most followed people on twitter (Top 500 from SocialBlade). If their tweet contains a company name/symbol, based on on the stocks symbols dataset, then we'll start monitoring the stock. We can also analyse the tweet and see if the tweet is positive or negative, and then based on that assume if the stock should be sold or bought.


![stocks_monitor 002](https://raw.githubusercontent.com/Minitour/BigDataHW4/master/screenshots/ss1.png)

![stocks_monitor 003](https://raw.githubusercontent.com/Minitour/BigDataHW4/master/screenshots/ss2.png)

## Demo
https://www.youtube.com/watch?v=z_6miocPdoI


## Architecture

![stocks_monitor 001](https://user-images.githubusercontent.com/17438617/50923621-1e52da00-1456-11e9-98be-07f80b430d77.jpeg)

Our system is composed of 4 layers:
- **The topics layer** (Twitter Service, IEX Service) which will be in charge of maintaining a socket based stream to each of its API providers.
- **The pipeline layer** (Spark Service) which will be in charge of processing and manipulating the data as well as storing it in-memory.
- **The business logic** layer (Flask Backend) which is the main backend for our frontend application. It will handle and render all the html files that will be served to the clients as well as handle requests from the clients. This layer will receive data from the pipeline via post requests and will keep store a state of the data in-memory or via cache if necessary.
- **The presentation layer** (Frontend Application), which is a simple web app which is rendered on the backend and creates a POST request every second to refresh the data on the graphs it contains.


## Technologies

- `python 3.6`

- python libs:
`bs4`
`flask`
`nltk`
`pyspark`
`requests`
`requests_oauthlib`
`sklearn`

- Node JS: 
`node.js v8.11`
`npm v5.6.0`


## Setup

1) Open the project with PyCharm
2) Run modules/backend/app.py
3) Run the IEX service `node modules/iex/app.js`
4) Run the twitter service: `modules/twitter/twitter_service.py`
5) Run the spark service: `modules/spark/spark_service.py` (run after all services have promoted that they are listening for incoming connections)
6) Visit http://localhost:5001/

It is important that the python files are executed from PyCharm.


