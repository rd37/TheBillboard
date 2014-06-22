'''
Created on Jun 21, 2014

@author: ronaldjosephdesmarais
'''

service_url = "0.0.0.0:8080/billboard"
#service_url = "134.117.57.145:8080/billboard"
un = "rd"
pw = "bhreagh"

import JSONFactory as jfac
from httplib2 import Http
from urllib import urlencode
import urllib2,urllib,json

class LocalityServiceApi():
    
    def __init__(self):
        print "Login to Locality Service Starting the User Session using %s %s"%(un,pw)
        msg = jfac.createLogin(un,pw)
        resp = self._sendHttpPost(msg,"system_login")
        print "%s"%resp
    
    def _sendHttpPost(self,msg,req):
        data2 = dict(jsonMsg=msg)
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        h = Http()
        resp, content = h.request("http://%s/%s/"%(service_url,req), "POST", urlencode(data2),headers )
        return content
        
    def add_user(self,lat,lng):
        print "add new user %s %s"%(lat,lng)
        msg = jfac.createAddUser(lat,lng)
        resp = self._sendHttpPost(msg,"request")
        resp_obj = json.loads(resp)
        return "%s"%resp_obj[0]['pk']
    
    def rem_user(self,id):
        print "remove user from db %s"%id
        msg = jfac.createRemUser(id)
        return self._sendHttpPost(msg,"request")
        
    def update_user(self,lat,lng,id):
        print "update user location at %s %s id is %s"%(lat,lng,id)
        msg = jfac.createUpdateUser(lat,lng,id)
        return self._sendHttpPost(msg,"request")
        
    def search_for_users(self,lat,lng,lat_rng,lng_rng):
        print "search for users in %s:%s , %s:%s"%(lat,lng,lat_rng,lng_rng)
        msg = jfac.createSearchUsers(lat,lng,lat_rng,lng_rng)
        resp = self._sendHttpPost(msg,"request")
        resp_obj = json.loads(resp)
        ret_obj=[]
        for obj in resp_obj:
            ret_obj.append(obj['pk'])
        return ret_obj
        
    