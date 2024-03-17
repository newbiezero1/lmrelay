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

    def get_entry_levels(self, message: str) -> list:
        entry_level = []
        lines = message.split('\n')
        for line in lines:
            if line.lower().find("entry: ") >=0:
                line = line.replace('$','')
                data  = line.split(' ')
                entries = data[1].split('-')
                entry_dif = float(entries[1]) - float(entries[0])
                for i in range(5):
                    entry_level.append(float(entries[0]) + entry_dif/4*i)
        return entry_level
