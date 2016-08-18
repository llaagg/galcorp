from lib.vs import videostar 
from lib.common import vault
from lib.common import instr
    

lg = instr.ConsoleLogger('*** VS ***:')

def updateSettting(ssid):
    lg.log( 'setting: '+ssid)

def getUserCreds():
    v = vault.Vault("user", "pass", 'cookie', updateSettting)
    return v

videoStarClient = videostar.VsClient(getUserCreds(), lg)
channels = videoStarClient.getChannels()    

print channels

# get id and get stream url

print videoStarClient.getUrl(108)