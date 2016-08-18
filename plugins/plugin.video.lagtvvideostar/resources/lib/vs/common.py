def log(msg, level=xbmc.LOGNOTICE):
    #return
    level = xbmc.LOGNOTICE
    print('VS: %s' % (msg))

    try:
        if isinstance(msg, unicode):
            msg = msg.encode('utf-8')
        xbmc.log('[SPECTO]: %s' % (msg), level)
    except Exception as e:
        try:
            #xbmc.log('Logging Failure: %s' % (e), level)
            a=1
        except: pass  # just give up
