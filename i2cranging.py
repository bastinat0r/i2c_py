#!/usr/bin/python
import smbus
import time
import struct

address = 0x71

i2c = smbus.SMBus(1)

fmt = '<BBHHH'
def convert_block_to_ranging(block):
    str = ''.join(map(chr, block))
    t = struct.unpack(fmt, str)
    d = {"status" : t[0], "dqf" : t[1], "range" : t[2], "addr1" : t[3], "addr2" : t[4]}
    return d

def read_ranging_result(addr):
    block = i2c.read_i2c_block_data(addr, 2, 8)
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

def start_ranging(addr, target=None):
    if target:
        i2c.write_word_data(addr, 1, target)
        return i2c.read_byte(addr)
    return (0 == i2c.read_byte_data(addr, 1))

def start_remote_ranging(addr, source=None, target=None):
    if source and target:
        i2c.write_block_data(addr, 3, source & 0xFF00, source & 0xFF, target & 0xFF00, target & 0xFF)
        return i2c.read_byte(addr)
    if source:
        i2c.write_word_data(addr, 3, source)
        return i2c.read_byte(addr)

    return (0 == i2c.read_byte_data(addr, 3))

def set_i2c_addr(addr, new_addr):
    i2c.write_byte_data(addr, 0xFE, new_addr)
    if(i2c.read_byte(addr) == 0):
        print "after reset device 0x%x will have address 0x%x" %(addr, new_addr)

def set_short_addr(addr, short_addr):
    """set short address for ranging node"""
    i2c.write_word_data(addr, 0xFD, short_addr)
    return (i2c.read_byte(addr) == 0)

def set_reflector_addr(addr, reflector_addr):
    """set reflector address for ranging node"""
    i2c.write_word_data(addr, 0xFC, reflector_addr)
    return (i2c.read_byte(addr) == 0)

def set_initiator_addr(addr, initiator_addr):
    """set initiator address for ranging node"""
    i2c.write_word_data(addr, 0xFB, initiator_addr)
    return (i2c.read_byte(addr) == 0)

def clear_device_i2c_buffer(addr):
    i2c.write_byte(addr, 0xFF)

def get_short_addr(addr):
    """get short address for ranging node"""
    return i2c.read_word_data(addr, 0xED)

def get_reflector_addr(addr):
    """get reflector address for ranging node"""
    return i2c.read_word_data(addr, 0xEC)

def get_initiator_addr(addr):
    """get initiator address for ranging node"""
    return i2c.read_word_data(addr, 0xEB)

def set_freq_start(addr, f_start):
    """set start of frequency range for ranging node"""
    i2c.write_word_data(addr, 0xCA, initiator_addr)
    return (i2c.read_byte(addr) == 0)

def set_freq_step(addr, f_step):
    """set step width of frequency range for ranging node"""
    i2c.write_word_data(addr, 0xCB, initiator_addr)
    return (i2c.read_byte(addr) == 0)

def set_freq_stop(addr, f_stop):
    """set stop of frequency range for ranging node"""
    i2c.write_word_data(addr, 0xCC, initiator_addr)
    return (i2c.read_byte(addr) == 0)

def set_antenna_div(addr, antenna_div):
    """ set antenna diversisty """
    antenna_div_value = 0
    if antenna_div:
        antenna_div_value = 1
    return i2c.read_byte_data(addr, 0xCD, antenna_div_value)
