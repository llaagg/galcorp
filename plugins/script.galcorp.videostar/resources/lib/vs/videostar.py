import json

class VsClient:
    CookieName = "netviapisessid"

    def __init__(self, creds, httpClient, logger = None):
        self.vault = creds
        self.lg = logger
        self.client = httpClient

    def getChannels(self):
        loginResult = self.login()
        co = self.getLoginCookie(loginResult)

        limiturl='https://api.videostar.pl/invitations/limit'
        limitResult = self.client.post(limiturl, requestCookie=co)

        channelList='https://api.videostar.pl/channels/list/ios-plus'
        channelResult = self.client.post(channelList, requestCookie=  co);
        channels = json.loads(channelResult["payload"])["channels"]

        cresult = self.extractChannels(channels)

        return cresult

    def tryOldSession(self):
        if(self.vault.ssId != None and self.vault.ssId!='' ):
            try:
                ss = self.vault.ssId
                self.lg.log("Trying to use old cookie: "+ss)
                limiturl='https://api.videostar.pl/invitations/limit'
                limitResult = self.client.post(limiturl, requestCookie=self.getLoginCookie(ss))
                if limitResult:

                    self.lg.log(str(limitResult["payload"]))
                    status = json.loads(limitResult["payload"])
                    if status["status"] == "ok":
                        return ss
            except:
                self.lg.exc()

        return None

    def login(self):
        """
        performs login action
        """

        oldSsid = self.tryOldSession()
        if(oldSsid!='' and oldSsid != None):
            return oldSsid
        

        loginUrl =  'https://api.videostar.pl/user/login'

        postParams = {}

        postParams['permanent']=1
        postParams['login'] = self.vault.userName
        postParams['password'] = self.vault.password


        if(self.vault.userName == None or self.vault.password == None):
            raise Exception("User credentials not provided")

        self.lg.log("Starting authentication as "+postParams['login'])

        loginResult = self.client.post(loginUrl, post=postParams)       

        if loginResult:
            status = json.loads(loginResult["payload"])

            if(status["status"] != "ok"):
                erm = status["errors"][0]["msg"]
                raise Exception("Videostar: " + erm)
            else:
                sessid = loginResult["cookies"][self.CookieName]
                self.storeCookie(sessid)

            return sessid
        else:
            raise Exception('Failed to authenticate')

    def storeCookie(self, cookie):
        self.vault.UpdateCookie(cookie)

    def extractChannels(self, channels):
        listing = []
        for c in channels:
            free = (c["access_status"] == "subscribed")
            lent=(c["slug"] , c["name"], c["id"], free , c["thumbnail"])
            listing.append( lent )
            
        return listing

    def showChannels(self, channels):
        for c in channels: 
            self.lg.log (c["slug"] + " " +c ["name"] +" "+ c['access_status' ])


    def getLoginCookie(self, ssid):
        c = {}
        c[self.CookieName] = ssid
        return c

    def getUrl(self, id):
        """
        gets stream url from api
        """
        getStreamUrl = 'https://api.videostar.pl/channels/get/%s?format_id=2' % id

        loginResult = self.login()

        getStream = self.client.post(getStreamUrl, requestCookie= self.getLoginCookie(loginResult) );
        

        result = json.loads(getStream['payload'])
        if result['status'] == 'ok':
            url = result['stream_channel']['url_base']
            result = self.client.post(url, requestCookie=self.getLoginCookie(loginResult))
            return result["url"]
        else:
            raise Exception("Failed to obtain stream url from videostar")
        
