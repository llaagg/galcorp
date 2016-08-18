from lib.vs import videostar 
from lib.common import vault
from lib.common import instr
    

lg = instr.ConsoleLogger('*** VS ***:')

def updateSettting(ssid):
    lg.log( 'setting: '+ssid)

def getUserCreds():
    v = vault.Vault("pgalezowski@gmail.com", "VsBudapestIsHungry!2", 'a00c121f9599a102a87ce1bd3539302b', updateSettting)
    return v

videoStarClient = videostar.VsClient(getUserCreds(), lg)
channels = videoStarClient.getChannels()    

print channels

# get id and get stream url

print videoStarClient.getUrl(108)