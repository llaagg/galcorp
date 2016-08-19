from lib.vs import videostar 
from lib.common import vault
from lib.common import instr, client


lg = instr.ConsoleLogger('*** VS ***:')

def updateSettting(ssid):
    lg.log( 'setting: '+ssid)

def getUserCreds():
    v = vault.Vault("pgalezowski@gmail.com", "VsBudapestIsHungry!2", '6d04f0cdfbb79485c50d3a5d2be5df4c', updateSettting)
    return v

videoStarClient = videostar.VsClient(getUserCreds(), client.HttpClient(), lg)
channels = videoStarClient.getChannels()    

#print channels

# get id and get stream url

print videoStarClient.getUrl(108)