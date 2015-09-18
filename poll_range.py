#!/usr/bin/python2.7
from i2cranging import *
import argparse

def auto_int(i):
    return int(i, 0)

queue = []

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='continuously read range from i2c ranging node')
    parser.add_argument('address', type=auto_int, help='i2c address of ranging node to be used')
    parser.add_argument('--time', type=float, default=1, help='time to wait between each ranging')
    parser.add_argument('--target', type=auto_int, help='ranging id of target node')
    args = parser.parse_args()
    while True:
        set_reflector_addr(args.address, args.target)
        try:
            start_ranging(args.address)
            range_result = read_ranging_result(args.address)
            queue.append((range_result['range'], range_result['dqf']))
            if(len(queue) > 10):
                queue.pop(0)
            sum = 0
            div = 0
            for i in queue:
                sum += i[0]
                div += i[1]
            if(div > 0):
                print "dqf: %i, range: %i, avg: %i" %(range_result['dqf'], range_result['range'], sum / len(queue))
        except IOError:
            print "i2c Error"
        time.sleep(args.time)
