# Migration Mongo

![](https://img.shields.io/badge/python-3.7-yellow)
![](https://img.shields.io/badge/FastAPI-0.55.1-009485)
![](https://img.shields.io/badge/pydantic-1.5.1-e92063)
![](https://img.shields.io/badge/asyncio-3.4.3-yellow)
![](https://img.shields.io/badge/mongodb-3.6-green)

This is the sample REST API based on FastAPI framework and MongoDb like a persistence layer and asyncio coroutines.

## Project includes:
* REST API base on [FastApi](https://fastapi.tiangolo.com/)
* [Pydantic](https://pydantic-docs.helpmanual.io/) models
* [AsyncIo](https://docs.python.org/3/library/asyncio.html)
* Persistence layer based on [Mongo DB](https://www.mongodb.com/)
* Unit test coverage (In progress)
* Postman collection to make using the project easier

## Deploy

The project includes *Dockerfile* and *docker-compose.yml*. So it works out of the box 😎

    cd project_path
    docker-compose up -d

## How to?

Well, first you need to get acquainted with the [structure of the project](./Structure.md).

Secondly, you can use CURL requests to the API or use the [Postman collection](https://drive.google.com/file/d/1TM_W-Qnj892NcbleIjUn-Nsy_GJlASU1/view?usp=sharing)

## Workloads examples

*List all workloads*

    curl http://127.0.0.1:80/workloads

*Create a new workload*

    curl -X POST http://127.0.0.1:80/workloads 
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

*Update thr workload*

    curl -X PATCH http://127.0.0.1:80/workloads/<workload_id>
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

*Delete workload*

    curl -X DELETE 'http://127.0.0.1:80/workloads/<workload_id>'

## Migrations examples

*Get all migration models*

    curl 127.0.0.1:80/migrations

*Create a new migration model*

**Note: this action assumes that we have added two workloads**

    curl -X POST http://127.0.0.1:80/migrations 
    -H 'Content-Type: application/json' 
    -d '
    {
        "source_id": "<source_workload_id>", 
        "state": "NOT_STARTED",
        "migration_target": {
            "cloud_credentials": {
                "user_name": "user", 
                "password": "password",
                "domain": "tst.com"
            }, 
            "cloud_type": "azure", 
            "target_vm_id": "<target_workload_id>"
        }, 
        "mount_points": [
            {
                "name": "C:\\", 
                "size": 229
            }
        ]
    }'

**Note: the migration accepts workloads identified by ids, so workloads should be created first.**

*Update the migration model*

    curl -X PATCH http://127.0.0.1:80/migrations/<migration_id>
    -H 'Content-Type: application/json' 
    -d '
    {
        "state": "NOT_STARTED",
        "source_id": "5eca7d5ed25d07212e4e5540",
        "migration_target": {
            "cloud_credentials": {
                "user_name": "user", 
                "password": "password",
                "domain": "tst.com"
                
            },
            "cloud_type": "vsphere",
            "target_vm_id": "5eca7dd9d25d07212e4e5543"
            
        }, 
        "mount_points": [
            {
                "name": "C:\\", 
                "size": 555
            }
        ]
    }'

*Delete migration*

    curl -X DELETE 'http://127.0.0.1:80/migrations/<migration_id>'

*Run migration*

    curl -X POST 'http://127.0.0.1:80/migrations/run/<migration_id>'

*Get the migration's state*

    curl http://127.0.0.1:80/migrations/state/<migration_id>
