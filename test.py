#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
from grafanaapi import GrafanaApi


url = "http://localhost:3000"
json = "apikey2.json"
itoken = os.environ.get("GRAFANA_TOKEN")
key, message= GrafanaApi.createApiKey(url, json, token=itoken)
print(key)
print(message)
keys = GrafanaApi.listApiKeys(url, token=itoken)
for key in keys:
    print(key)

json = "apifolder.json"
uid, message = GrafanaApi.createFolder(url, json, token=itoken)
print(uid)
print(message)

message = GrafanaApi.listFolders(url, token=itoken)    
print(message)

json = "apidashboard.json"
uid, message = GrafanaApi.createDashboard(url, json, token=itoken)
print(uid)
print(message)

message= GrafanaApi.listAllFoldersDashboards(url, token=itoken)
print(message)

json = "apidatasource.json"
id, message = GrafanaApi.createDatasource(url, json, token=itoken)
print(id)
print(message)

messge = GrafanaApi.listDatasources(url, token=itoken)
print(message)
