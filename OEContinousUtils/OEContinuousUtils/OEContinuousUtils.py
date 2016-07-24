# import os
import numpy as np
# import scipy.signal
# import scipy.io
# import time
# import struct
# from copy import deepcopy
import filecmp
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


if __name__ == '__main__':
    file_in = '/Users/fpbatta/dataLisa/rat27_plusmaze_base_II_2016-03-24_14-10-08/100_CH9.continuous'
    file_out = '/Users/fpbatta/dataLisa/rat27_plusmaze_base_II_2016-03-24_14-10-08/write_test'
    channel_data = OpE.loadContinuous(file_in, dtype=np.int16, trim_last_record=False)
    print(channel_data)
    hs = get_header_string(file_in)
    write_continuous(file_out, [channel_data, ], hs)
    channel_data2 = OpE.loadContinuous(file_out, dtype=np.int16)
    assert filecmp.cmp(file_in, file_out)
