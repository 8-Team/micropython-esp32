import network
import otp
import sh1106
import socket
import urequests
import utime

import settings
from hw_cfg import *


def wlan_connect():
    sta_if = network.WLAN(network.STA_IF)

    if not sta_if.isconnected():
        print('connecting to network...')

        sta_if.active(True)
        sta_if.connect(settings.WIFI_ESSID, settings.WIFI_PASSWORD)

        utime.sleep_ms(settings.WIFI_TIMEOUT)

    print('network config:', sta_if.ifconfig())
    return sta_if.isconnected()


def wlan_disconnect():
    sta_if = network.WLAN(network.STA_IF)

    if sta_if.isconnected():
        print('disconnecting from network...')

        sta_if.active(False)

        utime.sleep_ms(settings.WIFI_TIMEOUT)

    return sta_if.isconnected()


def call_bacotto(otp_gen):
    totp_tok = otp_gen.totp(utime.time(), interval=30)

    resp = urequests.get(settings.BACOTTO_URL + '/ping', params={
        'otp': totp_tok,
        'serial': settings.BACOTTO_SERIAL,
    })
    print('Wow! Bacotto replied:', resp.status_code, resp.text)


def run():
    if settings.DEBUG_HOST:
        debug_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    spi = machine.SPI(baudrate=100000, sck=sck_pin,
                      mosi=mosi_pin, miso=miso_pin)
    display = sh1106.SH1106_SPI(128, 64, spi, dc_pin, res_pin, cs_pin)
    display.sleep(False)

    display.text('Hello Otto!', 20, 30)

    otp_gen = otp.OTP(settings.BACOTTO_OTP_SECRET)
    sntp_setup = False

    while True:
        is_connected = wlan_connect()

        if is_connected:
            try:
                if not sntp_setup:
                    print('sntp setup...')
                    utime.settime_sntp()
                    sntp_setup = True

                if settings.DEBUG_HOST:
                    print('debug: sending display buffer to', settings.DEBUG_HOST)
                    debug_sock.sendto(display.buffer, (settings.DEBUG_HOST, 9999))
                    utime.sleep_ms(1000)

                print('current timestamp:', utime.time())
                call_bacotto(otp_gen)

            except Exception as e:
                print('Error:', e)
                utime.sleep_ms(1000)

            wlan_disconnect()
