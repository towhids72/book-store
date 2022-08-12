This is a simple example of microservices

It is using three microservices to create a simple bookstore API

Each microservice uses its own models and app configuration

# Usage:

    pip install -r requirements.txt

_for each microservice run:_

    flask db init
    flask db migrate
    flask db upgrade

# OR
simply run the docker-compose file, it contains all microservices migration and run commands