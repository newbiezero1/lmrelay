class Loma(object):
    def __init__(self):
        self.alert = {'pair': '',
                      'time': '',
                      'sl': '',
                      }
        pass

    def parse_alert(self, message: str):
        data = message.split(' ')
        if data[0].isupper():
            self.alert['pair'] = data[0]

        if data[1].find('sl') >= 0:
            sl_data = data[1].split('_')
            self.alert['time'] = sl_data[1]
            self.alert['sl'] = sl_data[2]
