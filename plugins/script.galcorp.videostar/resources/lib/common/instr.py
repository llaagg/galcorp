import sys

class ConsoleLogger:
    prefix = '-> '

    def __init__(self, prefix = ''):
        self.prefix = prefix+' '

    def log(self, msg):
        print self.prefix + msg

    def exc(self):
        self.log(str(sys.exc_info()[0]))