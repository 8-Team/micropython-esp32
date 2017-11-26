#!/usr/bin/env python3

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# data = bytearray(128 * 64 // 8)
# for i in range(len(data)):
#     data[i] = 0x00
# data[0] = 0xFF

data = bytearray(128 * 64 // 8)

# Hello
hello = b'\x00\x00\x00\xfe\xfe\x10\x10\xfe\xfe\x00\x00p\xf8\xa8\xa8\xb8\xb0\x00\x00\x00\x82\xfe\xfe\x80\x00\x00\x00\x00\x82\xfe\xfe\x80\x00\x00\x00p\xf8\x88\x88\xf8p'

for i, b in enumerate(hello):
    data[i] = b
    data[400 + i] = b
    data[700 + i] = b


print(len(data))
sock.sendto(data, ("127.0.0.1", 9999)) # framebuf.MONO_HLSB
print('sent...')
