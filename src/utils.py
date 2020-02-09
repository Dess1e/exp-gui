import os
from itertools import tee
from pathlib import Path
from datetime import datetime
from random import random
from string import digits


from PyQt5.QtWidgets import QFileDialog


def get_timestamp(fmt='%d-%m-%Y %H:%M:%S'):
    return datetime.now().strftime(fmt)


def gen_random_data(range_=5, num_of_points=2):
    return [random() * range_ for _ in range(num_of_points)]


def get_file_path_from_dialog():
    filename = QFileDialog.getOpenFileName()
    return filename


def serial_like_data_generator():
    from time import sleep
    sleep(0.3)
    return gen_random_data()


def find_device_path(device_name_part: str):
    """
    Returns path to serial device which name contains the specified substring.
    This is an easy way to look for available STM or Arduino connection.
    :param device_name_part: Substring to search in device names
    :return: The path to the device or None (if there is no such device)
    """
    path_to_find = '/dev/serial/by-id/'
    try:
        serial_devices = os.listdir(path_to_find)
    except FileNotFoundError:
        # this happens if there are no serial devices connected,
        # so the kernel doesn't even create this directory
        return None
    for device_name in serial_devices:
        if device_name_part in device_name:
            return str(Path(path_to_find) / device_name)
    else:
        return None


def filter_numerical_string(string: str) -> str:
    """
    Filters out non numerical characters from given string
    """
    return ''.join(list(filter(lambda x: x in digits, string)))


def pairwise(iterable):
    """s -> (s0,s1), (s1,s2), (s2, s3), ..."""
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

