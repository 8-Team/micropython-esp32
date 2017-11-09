import settings
import network
import otp
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


def call_bacotto(otp_gen):
    totp_tok = otp_gen.totp(utime.time(), interval=30)

    resp = urequests.get(settings.BACOTTO_URL + '/ping', params={
        'otp': totp_tok,
        'serial': settings.BACOTTO_SERIAL,
    })
    print('Wow! Bacotto replied:', resp.status_code, resp.text)


def run():
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

                print('current timestamp:', utime.time())
                call_bacotto(otp_gen)
            except Exception as e:
                print(e)
                utime.sleep_ms(1000)

            wlan_disconnect()
