from datetime import datetime


def get_timestamp(fmt='%d-%m-%Y %H:%M:%S'):
    return datetime.now().strftime(fmt)
