import sys

class KodiLogger:
    prefix = '-> '

    def __init__(self, dele, prefix = ''):
        self.prefix = prefix+' '
        self.dele =dele

    def log(self, msg):
        self.dele( self.prefix + msg)

    def exc(self):
        self.log(str(sys.exc_info()[0]))