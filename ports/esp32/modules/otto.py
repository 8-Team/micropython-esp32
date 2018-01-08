import otp
import sh1106
import socket
import urequests
import utime

import buttons
import icons
import settings
import wlan_manager

from hw_cfg import *


class Otto:
    def __init__(self):
        self._init_resources()
        self._init_state()

    def _init_resources(self):
        self.wlan = wlan_manager.WlanManager()

        self.spi = machine.SPI(baudrate=100000, sck=sck_pin,
                               mosi=mosi_pin, miso=miso_pin)

        self.display = sh1106.SH1106_SPI(128, 64, self.spi, dc_pin, res_pin, cs_pin)
        self.display.sleep(False)

        self.otp_gen = otp.OTP(settings.BACOTTO_OTP_SECRET)

        # buttons.Buttons(self.display)

        self.debug_sock = None
        if settings.DEBUG_ENABLED and settings.DEBUG_HOST:
            self.debug_sock = socket.socket(socket.AF_INET,
                                            socket.SOCK_DGRAM)

    def _init_state(self):
        self.start_time = None
        self.need_wifi_count = 0
        self.sntp_setup = False
        self.bacotto_ping_counter = 0

    def welcome(self):
        self.display.blit(icons.logo, 0, 0)
        self.display.show()
        utime.sleep_ms(2000)
        self.display.fill(0)

    def display_navbar(self):
        self.display.blit(icons.battery_half, 75, 0)
        if self.wlan.is_connected():
            self.display.blit(icons.wifi, 100, 0)

    def display_project(self):
        if not self.start_time:
            self.display.text('Fetching time...', 10, 40)
            return

        delta = utime.time() - self.start_time
        hours = int(delta / 3600)
        mins = int((delta % 3600) / 60)
        project = 'Otto'

        self.display.text(
            "%s %s:%s" % (project, _pretty_digit(hours), _pretty_digit(mins)),
            10, 30)

    def run(self):
        self.welcome()

        while True:
            self.display.fill(0)

            old_need_wifi_count = self.need_wifi_count
            if self.need_wifi_count > 0:
                self.wlan.connect()

            self.setup_sntp()

            try:
                self.debug()
            except Exception as exc:
                print('Error debug:', exc)

            try:
                self.ping_bacotto()
            except Exception as exc:
                print('Error ping_bacotto:', exc)
                utime.sleep_ms(1000)

            if old_need_wifi_count > 0 and self.need_wifi_count == 0:
                self.wlan.disconnect()
                utime.sleep_ms(100)

            self.display_navbar()
            self.display_project()

            self.display.show()
            utime.sleep_ms(100)

    def setup_sntp(self):
        if not self.sntp_setup:
            if self.wlan.is_connected():
                print('sntp setup...')
                utime.settime_sntp()
                self.sntp_setup = True
                self.need_wifi_count -= 1
                self.start_time = utime.time()
            else:
                self.need_wifi_count += 1

    def debug(self):
        if self.debug_sock:
            print('debug: sending display buffer to', settings.DEBUG_HOST)
            self.debug_sock.sendto(display.buffer, (settings.DEBUG_HOST, 9999))
            utime.sleep_ms(1000)

    def ping_bacotto(self):
        if self.bacotto_ping_counter == 9:
            if self.wlan.is_connected():
                self.bacotto_ping_counter = 0
                self.need_wifi_count -= 1
                self.call_bacotto()
            else:
                self.need_wifi_count += 1
        else:
            self.bacotto_ping_counter += 1

    def call_bacotto(self):
        if not self.wlan.is_connected():
            return

        # upy uses 2000 based epoch, but the backend does not
        now = utime.time() + utime.UPY_EPOCH_UNIX_EPOCH_DIFF

        print('current timestamp:', now)
        totp_tok = self.otp_gen.totp(utime.time(), interval=30)

        resp = urequests.get(settings.BACOTTO_URL + '/ping', params={
            'otp': totp_tok,
            'serial': settings.BACOTTO_SERIAL,
        })
        print('Wow! Bacotto replied:', resp.status_code, resp.text)


def _pretty_digit(d):
    if d <= 9:
        return '0' + str(d)

    return str(d)
