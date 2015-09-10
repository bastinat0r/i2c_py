#!/usr/bin/python
import smbus
import time
import struct

address = 0x71

i2c = smbus.SMBus(1)

fmt = '<BLBBB'
def convert_block_to_ranging(block):
    str = ''.join(map(chr, block))
    t = struct.unpack(fmt, str)
    d = {"status" : t[0], "range" : t[1], "dqf" : t[2], "addr1" : t[3], "addr2" : t[4]}
    return d

def read_ranging_result(addr):
    block = i2c.read_i2c_block_data(0x52, 2, 8)
    return convert_block_to_ranging(block)

def check_addr_for_device(addr):
    try:
      i2c.read_byte_data(addr, 0)
    except IOError:
      return False
    return True

def check_echo(addr, value):
    i2c.write_byte_data(addr, 0, value)
    return i2c.read_byte(addr)

def scan_addr_range():
    L = []
    for i in range(127):
        if(check_addr_for_device(i)):
            print("0x%x" %i)
            L.append(i)
    return L
    
def start_ranging(addr):
    return (0 == i2c.read_byte_data(addr, 1))

def set_i2c_addr(addr, new_addr):
    i2c.write_byte_data(addr, 0xFE, new_addr)
    if(i2c.read_byte(addr)):
        print "after reset device 0x%x will have address 0x%x" %(addr, new_addr)

