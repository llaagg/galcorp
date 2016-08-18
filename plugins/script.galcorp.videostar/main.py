import sys
from urlparse import parse_qsl
import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib.vs import videostar 
from resources.lib.common import  vault
from resources.lib.common import  kodiinstr


# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])

xbmsettings = xbmcaddon.Addon().getSetting

lg = kodiinstr.KodiLogger(xbmc.log,  '*** VS ***:')

def updateSettting(val):
    print "Updating user settings" + val
    xbmcaddon.Addon().setSetting("vspl_ssid", val)
    
    
def getUserCreds():
    v = vault.Vault(xbmsettings("vspl_username"),xbmsettings("vspl_password"), xbmsettings("vspl_ssid"), updateSettting)
    return v


def get_item(name, action, id = None, isFolder = False):
    """
    creates list item object
    @name to be visible on list
    @action to be called when selected
    @id - optional to pass as id to action
    @isFolder - specifies if the list item has sub items
    """
    #list_item = xbmcgui.ListItem( label = lti[0] )
        #http://mirrors.xbmc.org/docs/python-docs/15.x-isengard/xbmcgui.html#ListItem-setInfo
        #list_item.setInfo('video', {'title': lti[1]} )
        # list_item.setArt(	{'thumb': VIDEOS[category][0]['thumb'],
        #                         'icon': VIDEOS[category][0]['thumb'],
        #                         'fanart': VIDEOS[category][0]['thumb']})
        #url = '{0}?action=tv'.format(_url, lti[0])
        
    lti = xbmcgui.ListItem(label = name)
    #lti.setInfo('video', {'title': name} )
    url = '{0}?action={1}&id={2}'.format(_url, action, id)
    itm = (url, lti, isFolder)
    #xbmc.log( str( itm) )
    return itm

def settings():
    print "Lest setup the stuuf"
    pass

def watch(id):
    lg.log("Watching")
    videoStarClient = videostar.VsClient(getUserCreds(), lg)
    url = videoStarClient.getUrl(id)    
    xbmc.Player().play(url)

def list_free_channels():
    """
    lists all channels in video star
    """
    videoStarClient = videostar.VsClient(getUserCreds(), lg)
    list = videoStarClient.getChannels()
    
    listing = []

    for lti in list:
        if(lti[3] ):        
            listing.append(get_item(lti[1], "watch",lti[2]) )
    
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def list_channels():
    """
    lists all channels in video star
    """
    lg.log('Hi plugin started')

    xbmc.log('Listing channels')

    videoStarClient = videostar.VsClient(getUserCreds(), lg)
    list = videoStarClient.getChannels()
    
    listing = []

    for lti in list:
        listing.append(get_item(lti[1], "watch",lti[2]) )

    
    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def menu():
    """
    shows default menu
    """

    listing = []
    listing.append(  get_item("Availble channels", "availblechannels", isFolder = True) )
    listing.append(  get_item("All Channels", "allchannels", isFolder = True) )
    listing.append(  get_item("Settings", "settings", isFolder = True) )

    xbmcplugin.addDirectoryItems(_handle, listing, len(listing))
    #xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

    
def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring
    :param paramstring:
    """
    
    
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'allchannels':
            list_channels()
        if params['action'] == 'availblechannels':
            list_free_channels()
        elif params['action'] == 'settings':
            settings()
        elif params['action'] == 'watch':
            lg.log('Wathhing...')
            watch(params['id'])
        else:
            xbmc.log( str(params) )
    else:
        menu()

if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring
    router(sys.argv[2][1:])