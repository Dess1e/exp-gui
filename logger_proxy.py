from utils import get_timestamp


class LoggerProxy:
    def __init__(self, widget):
        self.buffer = ''
        self.widget = widget

    def log(self, info):
        ts = get_timestamp()
        self.buffer += '[{ts}]: {info}<br>'.format(ts=ts, info=info)
        self.widget.setHtml(self.buffer)

    def warn(self, info):
        ts = get_timestamp()
        self.buffer += '[{ts}]: <font color=\"Red\">{info}</font><br>'.format(ts=ts, info=info)
        self.widget.setHtml(self.buffer)