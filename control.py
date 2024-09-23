#!/usr/bin/env python3
import yaml
import logging
import argparse
from d700 import d700

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

def main():
    parser = argparse.ArgumentParser(
                    prog='D700 Controller',
                    description='Serial Control of a Kenwood D700',
                    epilog='')

    parser.add_argument("--config", dest='config', default='config.yml', help="The configuration file, default: config.yml")
    parser.add_argument("-l", "--list", action='store_true', help="List repeaters")
    parser.add_argument("-r", dest="repeater", help="Set repeater")

    args = parser.parse_args()

    with open(args.config, 'r') as file:
        repeaters = yaml.safe_load(file)

    if args.list: 
        print ("Defined Depeaters:")
        for repeater, setup in repeaters['repeaters'].items():
            print (f"{repeater}: {setup['rx']}")
    elif args.repeater:
        if args.repeater not in repeaters['repeaters']:
            print("Repeater not defined")
        else:
            d = d700(repeaters['port'])
            d.setRxFreq(repeaters['repeaters'][args.repeater]['rx'])
            d.setOffset(repeaters['repeaters'][args.repeater]['offset'])
            d.setTone(repeaters['repeaters'][args.repeater]['tone'])
    else: 
        parser.print_help()

main()