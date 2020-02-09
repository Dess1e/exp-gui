import json

from utils import get_timestamp


class DataController:
    def __init__(self, parent):
        self.parent = parent

    def save_data(self):
        threads = list(self.parent.serial_readers.values())
        data = {}
        for thread in threads:
            if not len(thread.x_data) or not len(thread.y_data):
                continue
            data_obj = {}
            name = data_obj
            data_obj['x_data'] = thread.x_data
            data_obj['y_data'] = thread.y_data
            data[name] = data_obj
            data_raw = json.dumps(data)
            open('{name}-{ts}.json'.format(name=name, ts=get_timestamp()), 'w').write(data_raw)

    def load_data(self, filename):
        """
        Loads saved data from json file
        This function should be called only if the serial reader threads are already initialized
        """
        dt = open(filename, 'r').read()
        obj = json.loads(dt)
        for tp in obj:
            reader = self.parent.serial_readers[tp]
            reader.x_data = obj[tp]['x_data']
            reader.y_data = obj[tp]['y_data']
