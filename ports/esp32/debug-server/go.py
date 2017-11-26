#!/usr/bin/env python3

# import socket
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# data = bytearray(128 * 64 / 8)
# for i in range(len(data)):
#     data[i] = 0xFF # 0x00
# sock.sendto(data, ("127.0.0.1", 9999)) # framebuf.MONO_HLSB

import threading
import tkinter as tk

import asyncio
from functools import partial


def main():
    tk_root = tk.Tk()
    Main(tk_root)
    tk_root.mainloop()


class Main:
    WIDTH = 128
    HEIGHT = 64
    PORT = 9999

    def __init__(self, tk_root):
        # Tk setup
        tk_root.title("Otto debug")

        self.canvas = tk.Canvas(tk_root, width=self.WIDTH, height=self.HEIGHT, bg="#000000")
        self.canvas.pack()

        self.img = tk.PhotoImage(width=self.WIDTH, height=self.HEIGHT)
        self.canvas.create_image((self.WIDTH / 2, self.HEIGHT / 2), image=self.img, state="normal")

        # Prepare coroutine to connect server
        self.transport = None # type: asyncio.DatagramTransport

        @asyncio.coroutine
        def _connect():
            loop = asyncio.get_event_loop()
            yield from loop.create_datagram_endpoint(lambda: self, local_addr=("0.0.0.0", self.PORT))

        # Thread that will handle io loop
        def _run(loop):
            asyncio.set_event_loop(loop)
            loop.run_forever()

        ioloop = asyncio.new_event_loop()
        asyncio.run_coroutine_threadsafe(_connect(), loop=ioloop) # Schedules connection
        t = threading.Thread(target=partial(_run, ioloop))
        t.daemon = True
        t.start() # Server will connect now

    def connection_made(self, transport):
        print("connection_made")
        self.transport = transport

    def connection_lost(self, exc):
        print("connection_lost")

    def datagram_received(self, data, addr):
        print("datagram_received", addr)

        # TODO: framebuf.MONO_VLSB
        for i, by in enumerate(data):
            for j in range(8):
                col = i % Main.WIDTH
                row = i // Main.WIDTH * 8 + j

                bit = (by >> j) & 0x1
                color = '#FFFFFF' if bit else '#000000'
                self.img.put(color, (col + 1, row + 1))

    def error_received(self, exc):
        print("error_received")


if __name__ == "__main__":
    main()
