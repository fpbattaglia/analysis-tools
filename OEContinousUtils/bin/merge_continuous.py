#!/usr/bin/env python

import argparse

from OEContinuousUtils.OEContinuousUtils import merge_channel


import argparse
parser = argparse.ArgumentParser(description='Merge OpenEphys Continuous files the timestamps are concatenated')
parser.add_argument(dest='channels',metavar='channel', nargs='+',
                    help='channels to be be merged')
parser.add_argument('-x', dest='replace', action='store_true',
                    help='replace existing merge file')
parser.add_argument('-d', dest='data_dir', action='store',
                    help='folder where data reside')


args = parser.parse_args()

for ch in args.channels:
    if args.replace:
        merge_channel(ch, data_dir=args.data_dir, remove_existing=True)
    else:
        try:
            merge_channel(ch, data_dir=args.data_dir)
        except FileExistsError:
            print('merged file exists, use -x to override')