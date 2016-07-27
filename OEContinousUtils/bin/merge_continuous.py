#!/usr/bin/env python

import argparse

from OEContinuousUtils.MergeUtils import merge_channel


import argparse
parser = argparse.ArgumentParser(description='Merge OpenEphys Continuous files the timestamps are concatenated')
parser.add_argument(dest='channels',metavar='channel', nargs='+',
                    help='channels to be be merged')
parser.add_argument('-x', dest='replace', action='store_true',
                    help='replace existing merge file')
parser.add_argument('-d', dest='data_dir', action='store',
                    help='folder where data reside')
parser.add_argument('-a', dest='do_aux', action='store_true',
                    help='do AUX files instead of CH files')


args = parser.parse_args()

if args.do_aux:
    sig_prefix = 'AUX'
else:
    sig_prefix = 'CH'

for ch in args.channels:
    if args.replace:
        merge_channel(ch, data_dir=args.data_dir, remove_existing=True, sig_prefix=sig_prefix)
    else:
        try:
            merge_channel(ch, data_dir=args.data_dir, sig_prefix=sig_prefix)
        except FileExistsError:
            print('merged file exists, use -x to override')