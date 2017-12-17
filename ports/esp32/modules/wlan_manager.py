import network
# import utime

import settings


# meant to be used as a singleton, but I don't bother doing it correctly...
class WlanManager:
    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)

        self._connecting = False

    def is_connected(self):
        return self.sta_if.isconnected()

    def connect(self):
        if not self._connecting and not self.is_connected():
            self._connecting = True
            self.sta_if.active(True)
            self.sta_if.connect(settings.WIFI_ESSID, settings.WIFI_PASSWORD)

            # utime.sleep_ms(settings.WIFI_TIMEOUT)
            print('connecting to network...')


    def disconnect(self):
        if self.is_connected():
            self._connecting = False
            self.sta_if.active(False)

            # utime.sleep_ms(settings.WIFI_TIMEOUT)
            print('disconnecting from network...')
