# Migration Mongo

![](https://img.shields.io/badge/python-3.7-yellow)
![](https://img.shields.io/badge/mongodb-3.6-green)
![](https://img.shields.io/badge/asyncio-3.4.3-yellow)

This is the sample REST API on the Flask framework based on MongoDb like a persistence layer and asyncio coroutines.

## Project includes:
* REST API
* [AsyncIo](https://docs.python.org/3/library/asyncio.html)
* Persistence layer based on [Mongo DB](https://www.mongodb.com/)
* Unit test coverage
* Postman collection to make using the project easier

Well, you could download a postman collection form [here](https://drive.google.com/file/d/1yNv2NFlbhsnT1wv3rCrGHtG9AbCKbcQL/view?usp=sharing)

## Workloads

### List all workloads (GET-request): 

        curl http://127.0.0.1:80/workloads

### Create new workload (POST-request):

        curl -X POST http://127.0.0.1:80/workloads 
         -H 'Cache-Control: no-cache' 
         -H 'Content-Type: application/json'   
         -d 'worload_object'

In result you will get the workload id like `5e9b1c836ca6be564403c673`
         
Workload object example:

    {
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
    }

### Update workload (PUT-request)

        curl -X PUT http://127.0.0.1:80/workloads/5e9b1c836ca6be564403c673
        -H 'Content-Type: application/json' 
        -d 'worload_object'

### delete workload (DELETE-request)

        curl -X DELETE 'http://127.0.0.1:80/workloads?id=0'

## Migrations

### list all migrations (GET-request):

        curl 127.0.0.1:80/migrations

### create new migration (POST-request):
**Note: migration accepts workloads identified by ids, so workloads should be created first.**

let's assume we added two workloads

    curl -X POST http://127.0.0.1:80/migrations 
    -H 'Content-Type: application/json' 
    -d 'migration_object'

Example of the migration object 

    {
        "source_id": "5e9b1a0aab2830c2284984f8", 
        "migration_target": {
            "cloud_credentials": {
                "user_name": "user", 
                "password": "password",
                "domain": "tst.com"
            }, 
            "cloud_type": "azure", 
            "target_vm_id": "5e9b1a4cab2830c2284984fa"
            
        }, 
        "mount_points": [
            {
                "name": "C:\\", 
                "size": 229
            }
        ]
    }

### Update migration (PUT-request)

        curl -X PUT http://127.0.0.1:80/migrations/<id>
        -H 'Content-Type: application/json' 
        -d 'migration_object'

### Delete migration (DELETE-request)

        curl -X DELETE 'http://127.0.0.1:80/migrations/<id>'

### Run migration (POST-request)

        curl -X POST 'http://127.0.0.1:80/migrations/run/<id>'

### Get migration state (GET-request)

        curl http://127.0.0.1:80/migrations/state/0
