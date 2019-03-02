# -*- coding: utf-8 -*-
"""
Update all autorec entries to delete wrong schedules 

Should be started after each restart of tvheadend.

  see https://tvheadend.org/issues/5056
  see https://tvheadend.org/issues/4454

@author: Arne Drees
"""

from tvh.htsp import HTSPClient
import json


def get_autorecs():
    HTSP.send('api', {'path': 'dvr/autorec/grid', 'args': {}})
    msg = HTSP.recv()
    return msg['response']['entries']

def upd_autorec(data):
    #args = { 'node': [ {'uuid': data['uuid'], 'content_type': data['content_type']} ] }
    args = { 'node': [ {'uuid': data['uuid'], 'minduration': data['minduration_new']} ] }

    HTSP.send('api', {
    'path': 'idnode/save',
    'args': args
    })
    return HTSP.recv()

def upd_all():
    #get all autorecs
    autorecs = get_autorecs()
    
    #update all without changing anything
    for autorec in autorecs:
        #print(json.dumps(autorec, indent=4, sort_keys=True))
        autorec['minduration_new'] = abs(autorec['minduration']//1-1)  #toggle between 1 and 0
        print('updating uuid', autorec['uuid'], autorec['name'])
        upd_autorec(autorec)

if __name__ == '__main__':
    #read config file
    try:
        with open('config.json', 'r') as config_file:
            CONFIG = json.load(config_file)
            HOSTNAME = CONFIG['hostname']
            #optional: try to read user and password
            try:
                USER = CONFIG['username']
                PASSWORD = CONFIG['password']
            except:
                pass
    except:  #error, use default settings
        print('ERROR: config.json does not exist or is wrong. Use localhost and no auth')
        HOSTNAME='localhost'
    
    #set up connector
    HTSP = HTSPClient((HOSTNAME, 9982))
    msg = HTSP.hello()
    
    #try to authenticate
    try:
        HTSP.authenticate(USER, PASSWORD)
        print('Authentification successful')
    except:
        print('Authentification skipped or failed - go on without auth')
    
    #update all recordings without really changing anything
    upd_all()

    #debug: print list of recordings
    #print(get_autorecs())
