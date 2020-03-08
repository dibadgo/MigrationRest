Starting rest:

launch rest.py with python3

## Workloads

1. list all workloads (GET-request): 

curl http://127.0.0.1:80/workloads

2. create new workload (POST-request):

curl -X POST http://127.0.0.1:80/workloads  -H 'Cache-Control: no-cache' -H 'Content-Type: application/json'   -d '{"ip": "8.800.777.38.38", "Credentials": {"user_name": "user", "password": 
"password", "domain": "tst.com"}, "Storage": [{"name": "C:\\", "size": 229}]}'

3. update workload (PUT-request)

curl -X PUT http://127.0.0.1:80/workloads -H 'Content-Type: application/json' -d '{"id": 1, "Credentials": {"user_name": "turbo_user", "password": "turbo_password", "domain": "tst.com"}}'

4. delete workload (DELETE-request)

curl -X DELETE 'http://127.0.0.1:80/workloads?id=0'

## Migrations

1. list all migrations (GET-request):

curl 127.0.0.1:80/migrations

2. create new migration (POST-request):

Note: migration accepts workloads identified by ids, so workloads should be created first.

let's assume we added two workloads, with ids 1 and 2

curl -X POST http://127.0.0.1:80/migrations -H 'Content-Type: application/json' -d '{"source_id": 1, "migration_target": {"cloud_credentials": {"user_name": "user", "password": "password", "domain": "tst.com"}, "cloud_type": "azure", "target_vm_id": 2}, "mount_points": [{"name": "C:\\", "size": 229}]}'

3. update migration (PUT-request)

curl -X PUT http://127.0.0.1:80/migrations -H 'Content-Type: application/json' -d '{"id": 0, "migration_target": {"cloud_credentials": {"user_name": "user", "password": "password", "domain": "tst.com"}, "cloud_type": "vsphere", "target_vm_id": 2}, "mount_points": [{"name": "C:\\", "size": 229}]}'

4. delete migration (DELETE-request)

curl -X DELETE 'http://127.0.0.1:80/migrations?id=0'

5. run migration (POST-request)

curl -X POST 'http://127.0.0.1:80/migrations/run?id=0'

6. get migration state (GET-request)

curl http://127.0.0.1:80/migrations/state/0
