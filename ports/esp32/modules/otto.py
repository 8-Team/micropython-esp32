import settings
import network
import urequests
import utime


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


def call_bacotto():
    resp = urequests.get(settings.BACOTTO_URL)
    print('Wow! Bacotto replied:', resp.text)


def run():
    while True:
        is_connected = wlan_connect()

        if is_connected:
            try:
                call_bacotto()
            except Exception as e:
                print(e)
                utime.sleep_ms(1000)

            wlan_disconnect()
