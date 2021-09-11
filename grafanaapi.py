#!/usr/bin/python3
# -*- coding: utf-8 -*-
from cryptography.fernet import Fernet
#from base64 import encode
import requests
from json import loads as jsonload



'''
grafanaapi.py is to be used by other python modules to automate grafana dashboards creation
by using some GrafanaApi functions like createApiKey...

'''

__version__ = "1.0.0"

ALLOWED_METHODS = ["DELETE", "GET", "POST", "PUT"]
ALLOWED_URL = ["http://", "https://"]
ALLOWED_AUTHENTICATION = ["basic", "token"]

class GrafanaApi():
    def __init__(self, api, method, url, user, pwd, jsonfile, authentication, isToken):
        self.api = api
        self.method = method
        self.json = jsonfile
        self.url = url
        self.user = user
        self.authentication = authentication
        self.pwd = GrafanaApi.crypted(pwd)
        self.istoken = isToken
        

    def __repr__(self):
        return (f"GrafanaApi api: {self.api}, method: {self.method}, url: {self.url}, authentication: {self.authentication}")

    #return the encrypted password/token
    @classmethod
    def crypted(cls, pwd):
        cls.privkey = Fernet.generate_key()        
        cipher_suite = Fernet(cls.privkey)
        ciphered_text = cipher_suite.encrypt(pwd.encode())
        cls.pwd = ciphered_text
        return cls.pwd

    #return the decrypted password/token
    @classmethod
    def decrypted(cls, pwd):
        cls.pwd = pwd
        cipher_suite = Fernet(cls.privkey)
        decrypted_text = cipher_suite.decrypt(cls.pwd)
        decrypted_text = decrypted_text.decode()
        return decrypted_text

    #execute the grafana api using a temp instance
    @staticmethod
    def runGrafana(api, method, url, user, password, json, auth, isToken):
        if password == None:
            response = jsonload('{"message": "Error : password or token missing!"}')
            return response 
        tempGrafana = GrafanaApi(api, method, url, user, password, json, auth, isToken )
        response = tempGrafana.grafanaAuthentication()
        tempGrafana = None
        return response       

    #create a folder
    @staticmethod
    def createFolder(url, json, user="admin", pwd="", token="", auth="basic"):
        uid = ""
        password, isToken = GrafanaApi.__checkTokenPassword(pwd, token)
        method = "POST"
        api = "/api/folders"
        response = GrafanaApi.runGrafana(api, method, url, user, password, json, auth, isToken)
        if 'uid' in response:
            uid = response['uid']
        return uid, response

    #return a list of folders
    @staticmethod
    def listFolders(url, user="admin", pwd="", token="", auth="basic"):
        password, isToken = GrafanaApi.__checkTokenPassword(pwd, token)
        method = "GET"
        api = "/api/folders"
        response = GrafanaApi.runGrafana(api, method, url, user, password, None, auth, isToken)
        return response

    #create the api key using the json file received in parameter
    @staticmethod
    def createApiKey(url, json, user="admin", pwd="", token="", auth="basic"):
        key = ""
        password, isToken = GrafanaApi.__checkTokenPassword(pwd, token)
        method = "POST"
        api = "/api/auth/keys"
        response = GrafanaApi.runGrafana(api, method, url, user, password, json, auth, isToken)
        if 'key' in response:
            key = response['key']
        #    message = response["message"]
        return key, response

    def __checkTokenPassword(pwd, token):
        isToken = False
        password = ""
        if pwd == "" or pwd == None:
            isToken = True
            password = token
        elif token == "" or pwd == None:
            isToken = False
            password = pwd
        return password, isToken       

    #return a list of api keys
    @staticmethod
    def listApiKeys(url, user="admin", pwd="", token="", auth="basic"):
        password, isToken = GrafanaApi.__checkTokenPassword(pwd, token)
        method = "GET"
        api = "/api/auth/keys"
        response = GrafanaApi.runGrafana(api, method, url, user, password, None, auth, isToken)
        return response

    #create the api key using the json file received in parameter
    @staticmethod
    def createDashboard(url, json, user="admin", pwd="", token="", auth="basic"):
        uid = ""
        password, isToken = GrafanaApi.__checkTokenPassword(pwd, token)
        method = "POST"
        api = "/api/dashboards/db"
        response = GrafanaApi.runGrafana(api, method, url, user, password, json, auth, isToken)
        if 'uid' in response:
            uid = response['uid']
        #    message = response["message"]
        return uid, response

    #create the datasource using the json file received in parameter
    @staticmethod
    def createDatasource(url, json, user="admin", pwd="", token="", auth="basic"):
        id = ""
        password, isToken = GrafanaApi.__checkTokenPassword(pwd, token)
        method = "POST"
        api = "/api/datasources"
        response = GrafanaApi.runGrafana(api, method, url, user, password, json, auth, isToken)
        if 'id' in response:
            id = response['id']
        #    message = response["message"]
        return id, response

    #list all datasources
    @staticmethod
    def listDatasources(url, user="admin", pwd="", token="", auth="basic"):
        password, isToken = GrafanaApi.__checkTokenPassword(pwd, token)
        method = "GET"
        api = "/api/datasources"
        response = GrafanaApi.runGrafana(api, method, url, user, password, None, auth, isToken)
        return response

    @staticmethod
    #list all folders and dashboards
    def listAllFoldersDashboards(url, user="admin", pwd="", token="", auth="basic"):
        password, isToken = GrafanaApi.__checkTokenPassword(pwd, token)
        method = "GET"
        api = "/api/search"
        response = GrafanaApi.runGrafana(api, method, url, user, password, None, auth, isToken)
        return response

    #call private function depending the authentication method defined, basic is the default
    def grafanaAuthentication(self):
        #print("grafanaAuthentication")
        if self.authentication == "basic":
            response = self.__grafanaBasicAuth()
        else:     
            response = self.__grafanaTokenAuth()
        return response

    #internal function that formats the url and calls the grafana apis using basic authentication
    def __grafanaBasicAuth(self):
        beginurl = self.url.split("//")[0]
        endurl = self.url.split("//")[1]
        if self.istoken:
            apiurl = beginurl + "//api_key:" + GrafanaApi.decrypted(self.pwd) + "@" + endurl + self.api
        else:            
            apiurl = beginurl + "//" + self.user + ":" + GrafanaApi.decrypted(self.pwd) + "@" + endurl + self.api
        #header="'Accept: application/json' "
        header = {}
        header['Accept'] = 'application/json'
        header['Content-Type'] = 'application/json'
        #print(apiurl)
        response = self.__grafanaDispatch(apiurl, header)


    #internal function that formats the url and calls the grafana apis using bearer/token authentication
    def __grafanaTokenAuth(self):
        apiurl = self.url + self.api  
        header = {}
        header['Accept'] = 'application/json'
        header['Content-Type'] = 'application/json'
        header['Authorization'] = "Bearer " + GrafanaApi.decrypted(self.pwd)  
        #print(apiurl)
        #print(header)
        response = self.__grafanaDispatch(apiurl, header)
        return response

    #internal function that calls the requests
    def __grafanaDispatch(self, apiurl, header):
        try:
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
        except requests.exceptions.RequestException as e:  
            raise SystemExit(e)           
        return response.json()
