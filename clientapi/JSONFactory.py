'''
Created on Jun 21, 2014

@author: ronaldjosephdesmarais
'''
import json

#{"request":"login_request","username":"rd","password":"bhreagh"}
def createLogin(un,pw):
    return '{"request":"login_request","username":"%s","password":"%s"}'%(un,pw)
    
#'{"request":"add_billboard","name":"RONS_test_bb","lat":-142.1111,"lng":48.7777}'
def createAddUser(lat,lng):
    return '{"request":"add_billboard","name":"tmp_name","lat":%s,"lng":%s}'%(lat,lng)

def createUpdateUser(lat,lng,id):
    return '{"request":"update_billboard","name":"tmp_name_updated","lat":%s,"lng":%s,"billboard_id":%s}'%(lat,lng,id)

def createRemUser(key):
    return '{"request":"remove_billboard","billboard_id":"%s"}'%(key)

def createSearchUsers(lat,lng,lat_rng,lng_rng):
    return '{"request":"search_billboards","latitude":%s,"longitude":%s,"lat_rng":%s,"lng_rng":%s}'%(lat,lng,lat_rng,lng_rng)