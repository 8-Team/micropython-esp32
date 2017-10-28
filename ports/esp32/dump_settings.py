#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import os


# -----------------------------------------------------------
# Settings Types
# -----------------------------------------------------------

def _str_setting(val):
    return "'''{}'''".format(val)

def _int_setting(val):
    return str(int(val))


# -----------------------------------------------------------
# Settings
# -----------------------------------------------------------

WIFI_SETTINGS = (
    ('WIFI_ESSID', _str_setting),
    ('WIFI_PASSWORD', _str_setting),
    ('WIFI_TIMEOUT', _int_setting),
)

BACOTTO_SETTINGS = (
    ('BACOTTO_URL', _str_setting),
)


# -----------------------------------------------------------
# Main
# -----------------------------------------------------------

def main():
    # in the future env could be a config file
    env = os.environ

    _dump_settings_group(env, 'Wifi', WIFI_SETTINGS)
    _dump_settings_group(env, 'Bacotto', BACOTTO_SETTINGS)


def _dump_settings_group(env, comment, settings):
    print('#', comment)

    for sett, ty in settings:
        val = ty(env[sett])
        print("{} = {}".format(sett, val))

    print()


if __name__ == '__main__':
    main()
