# ShowReviewApi

You can checkout the documentation [here](https://app.swaggerhub.com/apis-docs/Riowritesdocs/ShowReviewAPI/1.0.0)

This API is split into 3 microservices built using Django Framework and Django rest Framework, those 3 services are a Gateway, user and shows.
Gateway --> Is responsible for routing to services that can be added to using django built in admin page.
            Also contains a redis cache to save verified JWT token to reduce the amount of verify requests to the user, after one request for a certain                 endpoint, gateway save the token for a later use with expiration time.
            
User --> responsible for everything user related, from generating JWT tokens, to registering new users and getting user information.
         This service communicate with shows service through an RPC pattern built with RabbitMQ.
         
Shows --> responsible for everything shows related, Also contains a worker to handle Rabbitmq requests from user service
