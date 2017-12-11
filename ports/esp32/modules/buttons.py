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
            month if len(str(month)) > 1 else "0" + str(month)
            day if len(str(day)) > 1 else "0" + str(day)
            hour if len(str(hour)) > 1 else "0" + str(hour)
            minute if len(str(minute)) > 1 else "0" + str(minute)
            second if len(str(second)) > 1 else "0" + str(second)
            self.display.text("%s/%s/%s" % (day, month, year), 20, 20)
            self.display.text("%s:%s:%s" % (hour, minute, second), 20, 30)
        self.display.show()
        self.flag = not self.flag
        self.pulse = False

