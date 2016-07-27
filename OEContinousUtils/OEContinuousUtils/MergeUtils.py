import os
import numpy as np
# import scipy.signal
# import scipy.io
# import time
# import struct
# from copy import deepcopy
import glob
import OEContinuousUtils.OpenEphys as OpE


def get_header_string(filepath):
    f = open(filepath, 'rb')
    header_string = f.read(1024)
    f.close()
    return header_string


def write_continuous(filepath, ch, header_string):

    indices = np.arange(0, OpE.MAX_NUMBER_OF_RECORDS*OpE.SAMPLES_PER_RECORD, OpE.SAMPLES_PER_RECORD, np.dtype(np.int64))
    marker = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 255], np.int8)
    # open file to write the data
    f = open(filepath, 'wb')

    if not (type(ch) is list or type(ch) is tuple):
        ch = (ch,)

    f.write(header_string)  # copy the header of the first file
    for data in ch:
        t = data['timestamps'].astype('<i8')
        rec_numbers = data['recordingNumber'].astype('>u2')
        samples = data['data'].astype('>i2')
        n_samples = int(data['header']['blockLength'])
        if n_samples != OpE.SAMPLES_PER_RECORD:
            raise ValueError('illegal block size')
        n_samples = np.array((n_samples,), '<u2')
        n_records = len(data['recordingNumber'])

        for rec_in in range(n_records):
            t[rec_in].tofile(f)
            n_samples.tofile(f)
            rec_numbers[rec_in:rec_in+1].tofile(f)
            samples[indices[rec_in]:indices[rec_in+1]].tofile(f)
            marker.tofile(f)

    f.close()


def get_merge_channel_list(ch, data_dir=None, sig_prefix='CH'):
    file_list = []

    file_glob = '100_' + sig_prefix + str(ch)+'_?.continuous'
    if data_dir:
        file_glob = os.path.join(data_dir, file_glob)
    file_list = glob.glob(file_glob)
    file1 = '100_' + sig_prefix + str(ch) + '.continuous'
    if data_dir:
        file1 = os.path.join(data_dir, file1)
    file_list.insert(0, file1)
    return file_list


def merge_channel(ch, data_dir=None, remove_existing=False, sig_prefix='CH'):
    file_out = '100_' + sig_prefix + str(ch)+'_merged.continuous'
    if data_dir:
        file_out = os.path.join(data_dir, file_out)

    if os.path.isfile(file_out):
        if remove_existing:
            os.remove(file_out)
        else:
            raise FileExistsError('output file exists.')

    file_list = get_merge_channel_list(ch, data_dir, sig_prefix=sig_prefix)
    if len(file_list) <= 1:
        raise ValueError('there are less than two files to merge, nothing to do.')
    ch_data = []
    hs = get_header_string(file_list[0])
    for f in file_list:
        c = OpE.loadContinuous(f, dtype=np.int16, trim_last_record=False)
        ch_data.append(c)
    write_continuous(file_out, ch_data, hs)
