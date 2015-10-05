#!/usr/bin/python2.7
from i2cranging import *
import argparse

def auto_int(i):
    return int(i, 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='change frequency settings of ranging nodes')
    parser.add_argument('address', type=auto_int, help='i2c address of ranging node to be used')
    parser.add_argument('--freq_start', type=int, help='start frequency', required=True)
    parser.add_argument('--freq_step', type=int, help='step frequency', required=True)
    parser.add_argument('--freq_stop', type=int, help='stop frequency', required=True)

    parser.set_defaults(feature=False, num=-1)
    args = parser.parse_args()
    try:
        set_freq_start(addr, args.freq_start)
        set_freq_step(addr, args.freq_step)
        set_freq_stop(addr, args.freq_stop)
    except IOError:
        print "i2c Error"
    time.sleep(args.time)
