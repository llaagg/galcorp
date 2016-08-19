import sys
import urllib
import urllib2
import ssl
import cookielib
    

class HttpClient:
    def __init__(self):
        pass

    def post(self, url, post=None, headers=None, requestCookie=None):
        timeout = 60
        getCookies = True
        handlers = []
        cookies = None
        result = {}
        try:
            # setup headers
            try: headers.update(headers)
            except: headers = {}


            if not requestCookie == None:
                headers["cookie"]=self.getCookie(requestCookie)

            #setup ignore certificate
            ssl_context = ssl._create_unverified_context()

            if getCookies :
                cookies  = cookielib.LWPCookieJar()
                handlers += [urllib2.HTTPHandler(), urllib2.HTTPSHandler(context=ssl_context), urllib2.HTTPCookieProcessor(cookies)]
                opener = urllib2.build_opener(*handlers)
                opener = urllib2.install_opener(opener)
            else:
                handlers += [urllib2.HTTPSHandler(context=ssl_context)]
                opener = urllib2.build_opener(*handlers)
                opener = urllib2.install_opener(opener)

            if post is None:
                request = urllib2.Request(url, headers=headers)
            else:
                request = urllib2.Request(url, urllib.urlencode(post), headers=headers)

            response =  urllib2.urlopen(request, timeout=int(timeout))

            result["payload"] =response.read()
            result["url"] = response.geturl()
            if cookies :
                cResult = {}
                for c in cookies: 
                    cResult[c.name]=c.value            
                result["cookies"]=cResult
            else:
                result["cookies"] = None
            
        except:
            instr.log(sys.exc_info())
        
        return result


    def getCookie(self, cookies):
        cookie = []
        for c in cookies.keys(): 
            cookie.append('%s=%s' % (c, cookies[c]))
        cookie = "; ".join(cookie)
        return cookie