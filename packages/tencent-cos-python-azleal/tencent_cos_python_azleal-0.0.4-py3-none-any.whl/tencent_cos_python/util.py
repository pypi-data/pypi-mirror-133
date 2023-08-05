# -*- coding: utf-8 -*-
import os
import random
from datetime import time

TEMP_PATH = "/tmp/" if os.getenv("TEMP_PATH") is None else os.getenv("TEMP_PATH")


class Util(object):

    @staticmethod
    def ms_to_time(time_in_ms):
        ms = (time_in_ms % 1000) * 1000
        second = (time_in_ms // 1000) % 60
        minute = (time_in_ms // (1000 * 60)) % 60
        hour = (time_in_ms // (1000 * 60 * 60)) % 60
        return time(hour, minute, second, ms)

    @staticmethod
    def ms_to_srt_time_str(time_in_ms):
        return Util.ms_to_time(time_in_ms).isoformat(timespec='microseconds')[:-3]

    @staticmethod
    def get_random_str(length=12):
        alphabet = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        sa = []
        for i in range(length):
            sa.append(random.choice(alphabet))
        return ''.join(sa)

    @staticmethod
    def get_random_path(length=20, non_dot_ext=None):
        while True:
            p = os.path.join(TEMP_PATH, Util.get_random_str(length)) + ('.' + non_dot_ext if non_dot_ext is not None
                                                                        else '')
            if not os.path.exists(p):
                return p
