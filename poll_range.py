from i2cranging import *
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='continuously read range from i2c ranging node')
    parser.add_argument('address', help='i2c address of ranging node to be used')
    parser.add_argument('time', help='time to wait between each ranging')
    args = parser.parse_args()
    while True:
        start_ranging(args.address)
        read_ranging_result(args.address)
        time.sleep(args.time)
