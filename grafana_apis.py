#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet
#from base64 import encode
import requests
import os 
import argparse

'''
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




'''

__version__ = "1.0.0"

ALLOWED_METHODS = ["DELETE", "GET", "POST", "PUT"]
ALLOWED_URL = ["http://", "https://"]
ALLOWED_AUTHENTICATION = ["basic", "token"]

class GrafanaApis():
    def __init__(self, api, method, url, user, pwd, jsonfile, authentication, isToken):
        self.api = api
        self.method = method
        self.json = jsonfile
        self.url = url
        self.user = user
        self.authentication = authentication
        self.pwd = GrafanaApis.crypted(pwd)
        self.istoken = isToken

    def __repr__(self):
        return (f"GrafanaApis api: {self.api}, method: {self.method}, url: {self.url}, authentication: {self.authentication}")

    @classmethod
    def crypted(cls, pwd):
        cls.privkey = Fernet.generate_key()        
        cipher_suite = Fernet(cls.privkey)
        ciphered_text = cipher_suite.encrypt(pwd.encode())
        cls.pwd = ciphered_text
        return cls.pwd

    @classmethod
    def decrypted(cls, pwd):
        cls.pwd = pwd
        cipher_suite = Fernet(cls.privkey)
        decrypted_text = cipher_suite.decrypt(cls.pwd)
        decrypted_text = decrypted_text.decode()
        return decrypted_text

    @classmethod
    def createApiKey(cls):
        return cls(cls.grafanaAuthentication())

    #call private function depending the authentication method defined, basic is the default
    def grafanaAuthentication(self):
        #print("grafanaAuthentication")
        if self.authentication == "basic":
            response = self.__grafanaBasicAuth()
        else:     
            response = self.__grafanaTokenAuth()
        print(response)
        try:
            print(response.json())
        except:
            print("error during requests execution, see http response")
        return response


    def __grafanaBasicAuth(self):
        beginurl = self.url.split("//")[0]
        endurl = self.url.split("//")[1]
        if self.istoken:
            apiurl = beginurl + "//api_key:" + GrafanaApis.decrypted(self.pwd) + "@" + endurl + self.api
        else:            
            apiurl = beginurl + "//" + self.user + ":" + GrafanaApis.decrypted(self.pwd) + "@" + endurl + self.api
        #header="'Accept: application/json' "
        header = {}
        header['Accept'] = 'application/json'
        header['Content-Type'] = 'application/json'
        #print(apiurl)
        if self.method == "POST":
            contents= open(self.json, "rb")
            #note that we can use instead of data=contents json=contents but contents should be json
            response = requests.post(apiurl, data=contents, headers=header)
            contents.close()
        elif self.method == "GET":
            response = requests.get(apiurl)
        elif self.method == "PUT":
            contents= open(self.json, "rb")
            #print(apiurl)
            response = requests.put(apiurl, data=contents, headers=header )
            contents.close()
        elif self.method == "DELETE":
            response = requests.delete(apiurl)  
        return response

    def __grafanaTokenAuth(self):
        apiurl = self.url + self.api  
        header = {}
        header['Accept'] = 'application/json'
        header['Content-Type'] = 'application/json'
        header['Authorization'] = "Bearer " + GrafanaApis.decrypted(self.pwd)  
        #print(apiurl)
        #print(header)
        if self.method == "POST":
            contents = open(self.json, 'rb')
            response = requests.post(apiurl, data=contents,headers=header)
            contents.close()
        elif self.method == "GET":
            response = requests.get(apiurl, headers=header)
        elif self.method == "PUT":
            contents = open(self.json, 'rb')
            response = requests.put(apiurl, data=contents, headers=header)
            contents.close()
        elif self.method == "DELETE":
            response = requests.delete(apiurl, headers=header)  
        return response



def main(args):
    isOk = True
    api = args.api
    method = args.method
    url = args.url
    user = args.user
    password = args.password
    token = args.token
    jsonfile = args.jsonfile
    authentication = args.auth
    if user == None:
        user = 'admin'
    if password == None:
        password = os.environ.get('GRAFANA_PASSWORD')
    if token == None:
        token = os.environ.get('GRAFANA_TOKEN')   
    if password == None and token == None:
        print("password or token should be defined or their environment variables GRAFANA_TOKEN/GRAFANA_PASSWORD")             
        isOk = False
        return isOk
    isToken = False        
    password_or_token = ''
    if password != None:
        password_or_token = password
        isToken = False
    elif token != None:
        password_or_token = token
        isToken = True
    else:
        print("password or token should be defined or their environment variables GRAFANA_TOKEN/GRAFANA_PASSWORD")             
        isOk = False
        return isOk

    if jsonfile == None:
        jsonfile = ''
    if authentication == None:
        authentication = 'basic'                      
    if authentication != 'basic':
        if token == None:
            print("token mandatory with authentication token")             
            isOk = False
            return isOk                          
         
    #http://admin:admin@localhost:3000/api/org
    testgrafana = GrafanaApis(api, method, url, user, password_or_token, jsonfile, authentication, isToken)                
    testgrafana.grafanaAuthentication()
    print(testgrafana)
    return isOk


#check if api starts by the root context
def grafanaCheckAuthentication(authentication):
    isOk = False
    if authentication in ALLOWED_AUTHENTICATION:
        isOk = True
    return isOk


#check if method is one of allowed methods
def grafanaCheckMethod(method):
    isOk = False
    if method in ALLOWED_METHODS:
        isOk = True
    return isOk


#check if api starts by the root context
def grafanaCheckRoot(root):
    isOk = False
    if root[0]  == "/":
        isOk = True
    return isOk


#check if the url starts by the allowed url 
def grafanaCheckUrl(url):
    isOk = url.startswith(ALLOWED_URL[0])
    if not isOk:
        isOk = url.startswith(ALLOWED_URL[1])
    return isOk

def checkArguments(args):
    #check if api start with the root directory
    isOk = grafanaCheckRoot(args.api)
    if not isOk:
        print("api should start by the root context / expected at first character!")
        return isOk
    #check if method is an allowed method               
    isOk = grafanaCheckMethod(args.method)
    if not isOk:
        print(f"unknown method! method should be one of the following methods : {str(ALLOWED_METHODS)}")
        return isOk
    #check if     
    isOk = grafanaCheckUrl(args.url)
    if not isOk:
        print(f"unknown url! url should start by one of the following strings: {str(ALLOWED_URL)}")
        return isOk
    return isOk
                    

def grafanaApisVersion():
    return "GrafanaApis version : " + __version__


#starting code
if __name__ == "__main__":
    helpmethod = f"should contain one of the method to use : {str(ALLOWED_METHODS)}"
    helpurl = f"should start by {str(ALLOWED_URL)}"
    helpauthentication = f"if not defined the basic authentication is used by default. Values allowed: {str(ALLOWED_AUTHENTICATION)}. \
         Basic authentication can use password value or token value, token authentication uses only token value"
    parser = argparse.ArgumentParser(description="GrafanaApis is a python3 program that try to simplify the uses of grafana apis.")
    parser.add_argument('-V', '--version', help='Display the version of GrafanaApis', action='version', version=grafanaApisVersion())
    parser.add_argument('method', help = helpmethod)
    parser.add_argument('api', help='Api eg: /api/org should contain the root context / and if any api needs id values add them in the api eg: /api/dashboards/uid/I3mrXgInk ')
    parser.add_argument('url', help=helpurl)
    parser.add_argument('-u', '--user', help='grafana user', required=False)
    parser.add_argument('-p', '--password', help='password. If password is omitted, be sure that env. variable GRAFANA_PASSWORD is defined or defined token parameter value', required=False)
    parser.add_argument('-t', '--token', help='token. If token is omitted, be sure that env. variable GRAFANA_TOKEN is defined or defined password parameter value', required=False)
    parser.add_argument('-J', '--jsonfile', help='json file needed for POST method instead of a json plain text structure', required=False)
    #parser.add_argument('-j', '--json', help='json plain text structure for POST method instead of a json file', required=False )
    parser.add_argument('-a', '--auth', help=helpauthentication, required=False)
    args = parser.parse_args()
    
    
    isOk = checkArguments(args)
    if isOk:
        isOk = main(args)
        if isOk: 
            print("done!")

 