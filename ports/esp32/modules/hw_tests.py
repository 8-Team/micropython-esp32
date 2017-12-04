import machine
import time

import sh1106

from hw_cfg import *


def display():
    spi = machine.SPI(baudrate = 100000, sck=sck_pin,
                      mosi=mosi_pin, miso=miso_pin)
    display = sh1106.SH1106_SPI(128, 64, spi, dc_pin, res_pin, cs_pin)
    display.sleep(False)
    display.fill(1)
    display.show()
    time.sleep(1)

    for i in range(3):
        display.fill(0)
        display.show()
        time.sleep(0.4)
        display.text("Otto Test!", 2, 1)
        display.show()
        time.sleep(0.4)

    display.fill(0)
    display.show()
    time.sleep(1)

    for i in range(0,255, 10):
        display.fill(0)
        display.text("%s" % i, 2, 1)
        display.fill_rect(40, 10, 50, 40, 1)
        display.contrast(i)
        display.show()
        time.sleep(0.3)

    display.fill(0)
    display.text("Fine", 2, 1)
    display.show()
    time.sleep(1)

def icons(icons, x=0, y=0):
    spi = machine.SPI(baudrate = 100000, sck=sck_pin,
                      mosi=mosi_pin, miso=miso_pin)
    display = sh1106.SH1106_SPI(128, 64, spi, dc_pin, res_pin, cs_pin)
    display.sleep(False)
    display.blit(icons, x, y)
    display.show()


def viberBtn():
    while True:
        if user_btn_pin.value() == 1:
            print("btn: %s" % user_btn_pin.value())
            for i in range(2):
                viber_pin.value(1)
                time.sleep(0.5)
                viber_pin.value(0)
                time.sleep(0.5)

        if enc_btn_pin.value() == 0:
            print("enS: %s" % enc_btn_pin.value())
            break

def viber():
    for i in range(10):
        viber_pin.value(1)
        time.sleep(0.5)
        viber_pin.value(0)
        time.sleep(0.5)

def buttons():
    for i in range(60):
        print("btn: %s" % user_btn_pin.value())
        print("enA: %s" % enc_a_pin.value())
        print("enB: %s" % enc_b_pin.value())
        print("enS: %s" % enc_btn_pin.value())
        time.sleep(0.3)

