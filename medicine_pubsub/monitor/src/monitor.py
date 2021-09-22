import time, uuid
from redis.client import Redis
db = Redis(host='redis', decode_responses=True)
# cg = db.consumer_group('cgtabsmaker', ['tabsorders'])
# db.xadd('tabsorders', {'step': 'connecting_monitor'})

while True:

    allgroupsinfo = {}
    try:
        allgroupsinfo = db.xinfo_groups('tabsorders')
    except Exception:
        print('Stream does not exist')
        exit(1)

    groupinfo = {}
    for grp in allgroupsinfo:
        # print(grp)
        if(grp['name'] == 'cgtabsmaker'):
            groupinfo = grp
            break

    consinfo = db.xinfo_consumers('tabsorders', 'cgtabsmaker')

    allinfo = db.xinfo_stream('tabsorders')

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

    lastgen                  = allinfo['last-generated-id'].split('-')[0]
    lastdis                  = groupinfo['last-delivered-id'].split('-')[0]
    returned['grouplagms']   = int(lastgen) - int(lastdis)

    returned['consumcount']  = groupinfo['consumers']
    returned['grouppending'] = groupinfo['pending']
    returned['length']       = allinfo['length']


    print(returned)
    print('-'*50)
    
    time.sleep(2)