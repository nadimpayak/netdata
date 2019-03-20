# -*- coding: utf-8 -*-
# Description:
# Author: Ilya Mashchenko (l2isbad)
# SPDX-License-Identifier: GPL-3.0-or-later

import os

PATH = os.getenv('PATH', '/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin').split(':')

CHART_BEGIN = 'BEGIN {0} {1}\n'
CHART_CREATE = "CHART {0} '{1}' '{2}' '{3}' '{4}' '{5}' {6} {7} {8}\n"
DIMENSION_CREATE = "DIMENSION '{0}' '{1}' {2} {3} {4} '{5}'\n"
DIMENSION_SET = "SET '{0}' = {1}\n"


def setdefault_values(config, base_dict):
    for key, value in base_dict.items():
        config.setdefault(key, value)
    return config


def run_and_exit(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
        exit(1)
    return wrapper


def on_try_except_finally(on_except=(None, ), on_finally=(None, )):
    except_func = on_except[0]
    finally_func = on_finally[0]

    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception:
                if except_func:
                    except_func(*on_except[1:])
            finally:
                if finally_func:
                    finally_func(*on_finally[1:])
        return wrapper
    return decorator


def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@on_try_except_finally(on_except=(exit, 1))
def safe_print(*msg):
    """
    :param msg:
    :return:
    """
    print(''.join(msg))


def find_binary(binary):
    """
    :param binary: <str>
    :return:
    """
    for directory in PATH:
        binary_name = '/'.join([directory, binary])
        if os.path.isfile(binary_name) and os.access(binary_name, os.X_OK):
            return binary_name
    return None


def read_last_line(f):
    with open(f, 'rb') as opened:
        opened.seek(-2, 2)
        while opened.read(1) != b'\n':
            opened.seek(-2, 1)
            if opened.tell() == 0:
                break
        result = opened.readline()
    return result.decode()
