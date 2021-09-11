# grafana_apis

grafana apis example in python

## grafanaapi.py

It's a python module that you can include in your python module example with test.py

## grafana_apis.py

It's to use in command line (you can convert it with pytoc in exe module)
usage: grafana_apis.py [-h] [-V] [-u USER] [-p PASSWORD] [-t TOKEN] [-J JSONFILE] [-a AUTH] method api url

    GrafanaApis is a python3 program that try to simplify the uses of grafana apis.

    positional arguments:
    method                should contain one of the method to use : ['DELETE', 'GET', 'POST', 'PUT']
    api                   Api eg: /api/org should contain the root context / and if any api needs id values add them in
                            the api eg: /api/dashboards/uid/I3mrXgInk
    url                   should start by ['http://', 'https://']

    optional arguments:
    -h, --help            show this help message and exit
    -V, --version         Display the version of GrafanaApis
    -u USER, --user USER  grafana user
    -p PASSWORD, --password PASSWORD
                            password. If password is omitted, be sure that env. variable GRAFANA_PASSWORD is defined or
                            defined token parameter value
    -t TOKEN, --token TOKEN
                            token. If token is omitted, be sure that env. variable GRAFANA_TOKEN is defined or defined
                            password parameter value
    -J JSONFILE, --jsonfile JSONFILE
                            json file needed for POST method instead of a json plain text structure
    -a AUTH, --auth AUTH  if not defined the basic authentication is used by default. Values allowed: ['basic',
                            'token']. Basic authentication can use password value or token value, token authentication
                            uses only token value

some grafana apis usage with results example:

    GET /api/org
        python3 grafana_apis.py GET /api/org http://localhost:3000
        {'id': 1, 'name': 'Main Org.', 'address': {'address1': '', 'address2': '', 'city': '', 'zipCode': '', 'state': '', 'country': ''}}


    POST /api/auth/keys
        python3 grafana_apis.py POST /api/auth/keys http://localhost:3000 -J apikey.json
        {'id': 4, 'name': 'mykey2', 'key': 'eyZZZjoiY1k0cXRSRTNISFZVRmZMaGRWRjZnb3NEbEJTcVAxcFMiLCJuIjoibXlrZXkyIiwiaWQiOZZZ'}


    GET /api/auth/keys
        python3 grafana_apis.py GET /api/auth/keys http://localhost:3000
        {'id': 1, 'name': 'mykey', 'role': 'Admin'}, {'id': 2, 'name': 'mykey2', 'role': 'Admin', 'expiration': '2021-09-06T17:35:25Z'}


    POST /api/folders
        python3 grafana_apis.py POST /api/folders http://localhost:3000 -J apidashboard.json
        {'id': 1, 'uid': 'l3KqBxCMz', 'title': 'Testing', 'url': '/dashboards/f/l3KqBxCMz/testing', 'hasAcl': False, 'canSave': True,
            'canEdit': True, 'canAdmin': True, 'createdBy': 'admin', 'created': '2021-09-06T10:27:34Z', 'updatedBy': 'admin',
            'updated': '2021-09-06T10:27:34Z', 'version': 1}


    GET /api/folders
        python3 grafana_apis.py GET /api/folders http://localhost:3000
        [{'id': 1, 'uid': 'l3KqBxCMz', 'title': 'Testing'}]


    PUT /api/folders/:uid
        python3 grafana_apis.py PUT /api/folders/l3KqBxCMz http://localhost:3000 -J apifolderupdate.json
        {'id': 1, 'uid': 'l3KqBxCMz', 'title': 'testingUpdatedNew', 'url': '/dashboards/f/l3KqBxCMz/testingupdatednew',
        'hasAcl': False, 'canSave': True, 'canEdit': True, 'canAdmin': True, 'createdBy': 'admin', 'created': '2021-09-06T10:27:34Z',
        'updatedBy': 'admin', 'updated': '2021-09-06T11:24:35Z', 'version': 4}


    POST /api/dashboards/db
        python3 grafana_apis.py POST /api/dashboards/db http://localhost:3000 -J apidashboard.json
        {'id': 4, 'slug': 'new-dashboard', 'status': 'success', 'uid': 'gCMlMiI7z', 'url': '/d/gCMlMiI7z/new-dashboard', 'version': 1}


    GET /api/dashboards/uid/:uid
        python3 grafana_apis.py GET /api/dashboards/uid/I3mrXgInk http://localhost:3000
        {'meta': {'type': 'db', 'canSave': True, 'canEdit': True, 'canAdmin': True, 'canStar': True, 'slug': 'production-overview',
        'url': '/d/I3mrXgInk/production-overview', 'expires': '0001-01-01T00:00:00Z', 'created': '2021-09-06T17:48:36Z',
        'updated': '2021-09-06T17:48:36Z', 'updatedBy': 'Anonymous', 'createdBy': 'Anonymous', 'version': 1, 'hasAcl': False, 'isFolder': False, 'folderId': 1, 'folderUid': 'l3KqBxCMz', 'folderTitle': 'testingUpdatedNew', 'folderUrl': '/dashboards/f/l3KqBxCMz/testingupdatednew', 'provisioned': False, 'provisionedExternalId': ''}, 'dashboard': {'id': 3, 'refresh': '25s', 'schemaVersion': 16, 'timezone': 'browser', 'title': 'Production Overview', 'uid': 'I3mrXgInk', 'version': 1}}

    POST /api/datasources
        python3 grafana_apis.py POST /api/datasources http://localhost:3000 -J apidatasource.json
        {'datasource': {'id': 2, 'uid': 'Alp67mS7z', 'orgId': 1, 'name': 'test_datasource', 'type': 'mysql', 'typeLogoUrl': '',
        'access': 'proxy', 'url': 'http://localhost:3306', 'user': 'root', 'database': 'sys', 'basicAuth': False, 'basicAuthUser': '',
        'basicAuthPassword': '', 'withCredentials': False, 'isDefault': False, 'jsonData': {}, 'secureJsonFields': {},
        'version': 1, 'readOnly': False}, 'id': 2, 'message': 'Datasource added', 'name': 'test_datasource'}

    GET /api/datasources
        python3 grafana_apis.py GET /api/datasources http://localhost:3000

## todo

Forecast :

- create a python package for grafanaapi.py and put it on pypi
- add other grafana apis function example for datasource you can retrieve by id, by uid or by name...
- testing!
