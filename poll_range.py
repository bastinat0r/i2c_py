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
    parser.add_argument('--num', type=auto_int, help='number of readings to take')
    parser.add_argument('--distance', type=auto_int, help='distance value for csv file')
    parser.add_argument('--csv', dest='csv', action='store_true')
    parser.set_defaults(feature=False, num=-1)
    args = parser.parse_args()
    if args.csv:
        if args.distance:
            print "from, to, dqf, range, status, distance"
        else:
            print "from, to, dqf, range, status"
    num_measurements = 0
    while args.num < 0 or num_measurements < args.num:
        if(args.target):
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
            if args.csv:
                if args.distance:
                    print "%x, %x, %i, %i, %i, %i" %(range_result['addr1'],range_result['addr2'],range_result['dqf'], range_result['range'], range_result['status'], args.distance)
                else:
                    print "%x, %x, %i, %i, %i" %(range_result['addr1'],range_result['addr2'],range_result['dqf'], range_result['range'], range_result['status'])
            else:
                if(div > 0):
                    print "0x%x -> 0x%x, dqf: %i, range: %i, avg: %i, status: %i" %(range_result['addr1'],range_result['addr2'],range_result['dqf'], range_result['range'], sum / len(queue, range_result['status']))
            if(range_result['dqf'] > 0):
                num_measurements += 1
        except IOError:
            print "i2c Error"
        time.sleep(args.time)
