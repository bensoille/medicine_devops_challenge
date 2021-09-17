import time
from walrus import Database  # A subclass of the redis-py Redis client.
db = Database(host='redis')
stream = db.Stream('tabsorders')
# cg = db.consumer_group('cgtabsmaker', ['tabsorders'])

while True:


    allgroupsinfo = stream.groups_info()
    groupinfo = {}
    for grp in allgroupsinfo:
        # print(grp)
        if(grp['name'].decode() == 'cgtabsmaker'):
            groupinfo = grp
            break

    consinfo = stream.consumers_info('cgtabsmaker')

    allinfo = stream.info()

    returned = {}
    print('='*25)
    print(allgroupsinfo)
    print('-'*25)
    print(groupinfo)
    print('-'*25)
    print(consinfo)
    print('-'*25)
    print(allinfo)
    print('-'*25)

    lastgen                  = allinfo['last-generated-id'].decode().split('-')[0]
    lastdis                  = groupinfo['last-delivered-id'].decode().split('-')[0]
    returned['grouplagms']   = int(lastgen) - int(lastdis)

    returned['consumcount']  = groupinfo['consumers']
    returned['grouppending'] = groupinfo['pending']
    returned['length']       = allinfo['length']


    print(returned)
    print('-'*50)
    
    time.sleep(2)