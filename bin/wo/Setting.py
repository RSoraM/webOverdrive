class Setting(object):
    setting = {
        'headers': {
            'user-agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
        },
        'delay': 3
    }

    def __init__(self, setting={}):
        if setting != {}:
            self.setting = setting

    def getHeader(self):
        return self.setting['headers']

    def setHeader(self, header):
        self.setting['headers'] = header

    def getDelay(self):
        return self.setting['delay']

    def setDelay(self, delay):
        self.setting['delay'] = delay
