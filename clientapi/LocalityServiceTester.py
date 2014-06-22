'''
Created on Jun 21, 2014

@author: ronaldjosephdesmarais
'''

#!/usr/bin/python

import sys, getopt

from clientapi.LocalityServiceApi import LocalityServiceApi

def main(argv):
   api = LocalityServiceApi()
   resp = api.add_user(48.76,-123.89)
   print "add user response %s, now remove it"%resp
   resp2 = api.rem_user(resp)
   print "remove user response %s"%resp2
   id = api.add_user(48.76,-123.89)
   print "add another user response %s, now update it"%id
   resp3 = api.update_user(48.75,-123.90,id)
   print "update user response %s, now lets do a search "%resp3
   resp4 = api.search_for_users(48.65,-123.80,0.15,0.15)
   print "users in range %s"%resp4

if __name__ == "__main__":
   main(sys.argv[1:])