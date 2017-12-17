from hw_cfg import *
import machine
import utime
import icons

class Buttons:
    def __init__(self, d):
        self.display = d
        self.flag = True
        self.pulse = False
        user_btn_pin.irq(self.__pulse, trigger=machine.Pin.IRQ_RISING)
        print("init buttons module")
        self.welcome()

    def __pulse(self, b):
        print(b)
        if not self.pulse:
            self.pulse = True
            self.show_time()

    def welcome(self):
        self.display.blit(icons.logo, 0, 0)
        self.display.show()
        utime.sleep_ms(2000)
        self.display.fill(0)
        self.display.text('Hello Otto!', 20, 30)
        self.display.show()
        utime.sleep_ms(1000)
        self.display.fill(0)
        self.display.show()

    def show_time(self):
        utime.sleep_ms(100)
        self.display.fill(0)
        if self.flag:
            self.display.blit(icons.logo, 0, 0)
            self.display.show()
            utime.sleep_ms(1000)
            self.display.fill(0)
            year, month, day, hour, minute, second, _, _ = utime.localtime()
            month = _pretty_digit(month)
            day = _pretty_digit(day)
            hour = _pretty_digit(hour)
            minute = _pretty_digit(minute)
            second = _pretty_digit(second)
            self.display.text("%s/%s/%s" % (day, month, year), 35, 20)
            self.display.text("%s:%s:%s" % (hour, minute, second), 35, 30)
        self.display.show()
        self.flag = not self.flag
        self.pulse = False


def _pretty_digit(d):
    if d <= 9:
        return '0' + str(d)

    return str(d)
