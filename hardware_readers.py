import serial


class Reader:
    ...


class ArduinoReader(Reader):
    def __init__(self, path):
        self.serial = serial.Serial(path, baudrate=38400)

    def read(self):
        data = self.serial.read_until(b'txend')
        return self.parse_data(data)

    def parse_data(self, data):
        try:
            data = data.decode('utf8').replace('txend', '')
            blocks = list(filter(lambda b: len(b) > 3, data.split('\r\n')))
            res = [float(b.split(': ')[1]) for b in blocks]
            if len(res) != 4:
                return None
            return {
                'x_data': res[0],
                'y_data': res[1],
                'aux_data': {
                    'some_data1': res[2],
                    'some_data2': res[3],
                }
            }
        except:
            return None

    def __del__(self):
        self.serial.close()


if __name__ == '__main__':
    r = ArduinoReader('/dev/ttyACM0')
    while True:
        print(r.read())