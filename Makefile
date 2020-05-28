deploy:
    docker-compose -f docker-compose.yml up rest mongo -d --build

deploy-mongo:
    docker-compose -f docker-compose.yml up mongo

rebuild-rest:
    docker-compose -f docker-compose.yml up rest -d --build

down:
    docker-compose -f docker-compose.yml down