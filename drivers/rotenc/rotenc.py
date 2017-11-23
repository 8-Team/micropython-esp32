"""Rotary encoder module for Micropython
"""

from machine import Pin

class RotaryEncoder:
    def __init__(self, ch_a, ch_b):
        if ch_a is None or ch_b is None:
            raise Exception("only AB encoder mode is supported yet")

        self.ch_a = ch_a
        self.ch_b = ch_b

        # init GPIOs as inputs
        self.ch_a.init(Pin.IN)
        self.ch_b.init(Pin.IN)

        # we only need to listen on a single line
        self.ch_a.irq(self.isr, trigger=Pin.IRQ_FALLING)

    def isr(self, pin):
        if self.ch_b.value() == 0:
            print("right")
        else:
            print("left")
