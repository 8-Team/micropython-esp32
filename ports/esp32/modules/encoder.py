from machine import Pin

import time


class Encoder(object):
    def __init__(self, pin_a, pin_b):

        self.pin_a = pin_a
        self.pin_b = pin_b

        # The following variables are assigned to in the interrupt callback,
        # so we have to allocate them here.
        self._value = None
        self._last_set_time = None

        self.set_callbacks(self._callback)

    def _callback(self, line):
        vala = self.pin_a.value()
        valb = self.pin_b.value()

        # ignore transitions, only a single pin should be 0
        if vala == valb:
            return

        self._value = 1 if vala else -1
        self._last_set_time = time.ticks_ms()

    def set_callbacks(self, callback=None):
        mode = Pin.IRQ_FALLING
        self.irq_clk = self.pin_a.irq(trigger=mode, handler=callback)
        self.irq_dt = self.pin_b.irq(trigger=mode, handler=callback)

    def close(self):
        self.set_callbacks(None)
        self.irq_clk = None
        self.irq_dt = None

    def get_value(self):
        if self._last_set_time is None:
            return None

        if time.ticks_diff(time.ticks_ms(), self._last_set_time) < 50:
            return None

        return self._value

    def reset(self):
        self._value = None
        self._last_set_time = None

