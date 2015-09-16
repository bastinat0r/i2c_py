#!/usr/bin/python2.7
from i2cranging import *
import argparse

def auto_int(i):
    return int(i, 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='continuously read range from i2c ranging node')
    parser.add_argument('address', type=auto_int, help='i2c address of ranging node to be used')
    parser.add_argument('--time', type=float, default=1, help='time to wait between each ranging')
    args = parser.parse_args()
    while True:
        start_ranging(args.address)
        print read_ranging_result(args.address)
        time.sleep(args.time)
