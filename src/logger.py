from utils import get_timestamp


class Logger:
    _instance = None

    def __init__(self, log_fun):
        self.buffer = ''
        self.log_fun = log_fun
        Logger._instance = self

    @classmethod
    def log(cls, info):
        ts = get_timestamp()
        cls._instance.buffer += '[{ts}]: {info}<br>'.format(ts=ts, info=info)
        cls._instance.log_fun(cls._instance.buffer)

    @classmethod
    def warn(cls, info):
        ts = get_timestamp()
        cls._instance.buffer += '[{ts}]: <font color=\"Red\">{info}</font><br>'.format(ts=ts, info=info)
        cls._instance.log_fun(cls._instance.buffer)


    @classmethod
    def clear_buffer(cls):
        cls._instance.buffer = ''
        cls._instance.log_fun(cls._instance.buffer)
