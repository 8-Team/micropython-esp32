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
