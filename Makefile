# Deployment

COMPOSE_FILE=docker-compose.yml

deploy:
    docker-compose -f $(COMPOSE_FILE) up rest mongo -d --build

deploy-mongo:
    docker-compose -f $(COMPOSE_FILE) up mongo -d

rebuild-rest:
    docker-compose -f $(COMPOSE_FILE) up rest --build

down:
    docker-compose -f $(COMPOSE_FILE) down

# REST calls

DOMAIN=http://127.0.0.1:80

workloads:
    curl $(DOMAIN)/workloads

create-workload:
    curl -X POST $(DOMAIN)/workloads
     -H 'Cache-Control: no-cache'
     -H 'Content-Type: application/json'
     -d '{
        "ip": "1.1.1.1",
        "Credentials": {
            "user_name": "user",
            "password": "password",
            "domain": "tst.com"
        },
        "Storage": [
            {
                "name": "C:\\",
                "size": 11
            },
            {
                "name": "D:\\",
                "size": 222
            }
        ]
    }'

update-workload: create-workload

    curl -X PATCH $(DOMAIN)/workloads/<workload_id>
    -H 'Content-Type: application/json'
    -d '{
        "ip": "1.1.1.1",
        "Credentials": {
            "user_name": "user",
            "password": "password",
            "domain": "tst.com"
        },
        "Storage": [
            {
                "name": "C:\\",
                "size": 11
            },
            {
                "name": "D:\\",
                "size": 222
            }
        ]
    }'

delete-workload:
    curl -X DELETE $(DOMAIN)/workloads/<workload_id>

