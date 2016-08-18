class Vault:
    def __init__(self, userName, password, ssId, updater):
        self.userName = userName
        self.password = password
        self.ssId = ssId
        self.updater = updater
    
    def UpdateCookie(self, cookie):
        self.ssId = cookie
        self.updater(cookie)