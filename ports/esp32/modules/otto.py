import otp
import sh1106
import socket
import urequests
import utime

# import buttons
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
        self.button = user_btn_pin

        self.debug_sock = None
        if settings.DEBUG_ENABLED and settings.DEBUG_HOST:
            self.debug_sock = socket.socket(socket.AF_INET,
                                            socket.SOCK_DGRAM)

    def _init_state(self):
        self.project_start_time = None
        self.need_wifi_count = 0
        self.sntp_setup = False
        self.bacotto_ping_counter = 0

        # stub
        self.current_project = None
        self.project_list = []
        self.project_idx = 0

        # hours to send to bacotto
        self.projects_hours = []

    def welcome(self):
        self.display.blit(icons.logo, 0, 0)
        self.display.show()
        utime.sleep_ms(2000)
        self.display.fill(0)

    def display_navbar(self):
        self.display.blit(icons.battery_half, 75, 0)
        if self.wlan.is_connected():
            self.display.blit(icons.wifi, 100, 0)

    def display_initializing(self):
        self.display.text('Fetching time...', 10, 40)

    def display_project_list(self):
        # TODO: scrolling
        for i, prj in enumerate(self.project_list[:3], start=1):
            name = prj['ShortName']
            self.display.text(name, 5, 15 + i * 10)

    def display_project_time(self):
        delta = utime.time() - self.project_start_time
        hours = int(delta / 3600)
        mins = int((delta % 3600) / 60)
        project = self.current_project

        self.display.text(
            "%s %s:%s" % (project['ShortName'], _pretty_digit(hours), _pretty_digit(mins)),
            10, 30)

    def display_body(self):
        if not self.sntp_setup:
            self.display_initializing()
            return

        if self.current_project is not None:
            self.display_project_time()
        else:
            self.display_project_list()

    def run(self):
        self.welcome()

        while True:
            self.display.fill(0)

            if self.current_project is None and self.button.value():
                self.project_start_time = utime.time()
                self.current_project = self.project_list[self.project_idx]
            elif self.current_project is not None and self.button.value():
                self.register_current_project()
                self.current_project = None
                self.project_start_time = None

            old_need_wifi_count = self.need_wifi_count
            if self.need_wifi_count > 0:
                self.wlan.connect()

            self.setup_sntp()
            self.fetch_projects()

            try:
                self.debug()
            except Exception as exc:
                print('Error debug:', exc)

            self.send_hours()

            # try:
            #     self.ping_bacotto()
            # except Exception as exc:
            #     print('Error ping_bacotto:', exc)
            #     utime.sleep_ms(1000)

            if old_need_wifi_count > 0 and self.need_wifi_count == 0:
                self.wlan.disconnect()
                utime.sleep_ms(500)

            self.display_navbar()
            self.display_body()

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

    def fetch_projects(self):
        # TODO: invalidate the list of projects
        if self.project_list:
            return

        if self.wlan.is_connected():
            print('fetching projects...')
            self.project_list = self.call_bacotto('GET', '/projects', {}).json()
            self.need_wifi_count -= 1
        else:
            self.need_wifi_count += 1

    def debug(self):
        if self.debug_sock:
            print('debug: sending display buffer to', settings.DEBUG_HOST)
            self.debug_sock.sendto(display.buffer, (settings.DEBUG_HOST, 9999))
            utime.sleep_ms(1000)

    def register_current_project(self):
        project_delta = utime.time() - self.project_start_time
        self.projects_hours.append((self.current_project, project_delta))

    def send_hours(self):
        if not self.projects_hours:
            return

        if self.wlan.is_connected():
            print('sending hours to bacotto')
            # self.call_bacotto('POST', 'register', {})
            self.projects_hours = []
            self.need_wifi_count -= 1
        else:
            self.need_wifi_count += 1

    def ping_bacotto(self):
        if self.bacotto_ping_counter == 9:
            if self.wlan.is_connected():
                self.bacotto_ping_counter = 0
                self.need_wifi_count -= 1
                self.call_bacotto('GET', '/ping', {})
                self.call_bacotto()
            else:
                self.need_wifi_count += 1
        else:
            self.bacotto_ping_counter += 1

    def call_bacotto(self, method, path, params):
        if not self.wlan.is_connected():
            return

        # upy uses 2000 based epoch, but the backend does not
        now = utime.time() + utime.UPY_EPOCH_UNIX_EPOCH_DIFF

        print('current timestamp:', now)
        totp_tok = self.otp_gen.totp(utime.time(), interval=30)

        params.update({
            'otp': totp_tok,
            'serial': settings.BACOTTO_SERIAL,
        })

        if method in ('POST', 'PUT'):
            resp = urequests.request(method, settings.BACOTTO_URL + path, json=params)
        else:
            resp = urequests.request(method, settings.BACOTTO_URL + path, params=params)

        print('Wow! Bacotto replied:', resp.status_code, resp.text)

        return resp


def _pretty_digit(d):
    if d <= 9:
        return '0' + str(d)

    return str(d)
