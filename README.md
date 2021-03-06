# FLASK MICROSERVICES

This is a solution implemented for the problem. 
https://drive.google.com/file/d/1eHNjso1a8TlXDUXtmVlv__bBI6P8CVA3/view

## How to run it
1. Download and install docker.
2. Download and install docker-compose.
3. Open root directory in the terminal and run `sudo docker-compose -f docker-compose.yml up --build`
4. The server will start running on port **8080** localhost. Free the port or change Nginx configuration file to a suitable port.
5. Open `http://localhost:8080/docs` to view documention.

## Information
1. Use the *test.csv* file included in helpers folder to check data ingestion process.
2. Use the postman collection in helpers folder to test the API.


## HLD LLD
High Level Desgign: https://drive.google.com/file/d/1YkiyqM7bGDho6GhQ6p1ISH2IjB-z_4Xu/view?usp=sharing

Low Level Desing: https://drive.google.com/file/d/16dtgEZP5OEVjw3XGBn67n67ZtbhZKOqs/view?usp=sharing

Open the file with **app.diagrams.net** to view and understand the High Level and Low Level design of the APIs.

## Further improvements
You can try implementing the following features, I'll do it in sometime, probably:
1. Add logging functionality.
2. Unit tests (at least).
3. Functional tests for cross service APIs.
4. Design a better sorting mechanism for sort contents by reads and likes.
5. Add pagination for the contents.
6. Improve documenation to include error responses.

You can add your suggestion with a PR too.