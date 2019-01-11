![stocks_monitor 001](https://user-images.githubusercontent.com/17438617/50923621-1e52da00-1456-11e9-98be-07f80b430d77.jpeg)

Our system is composed of 4 layers:
- **The topics layer** (Twitter Service, IEX Service) which will be in charge of maintaining a socket based stream to each of its API providers.
- **The pipeline layer** (Spark Service) which will be in charge of processing and manipulating the data as well as storing it in-memory.
- **The business logic** layer (Flask Backend) which is the main backend for our frontend application. It will handle and render all the html files that will be served to the clients as well as handle requests from the clients. This layer will receive data from the pipeline via post requests and will keep store a state of the data in-memory or via cache if necessary.
- **The presentation layer** (Frontend Application), which is a simple web app which is rendered on the backend and creates a POST request every second to refresh the data on the graphs it contains.
