import unittest
import os.path
import filecmp
import numpy as np
from numpy.testing import assert_array_equal as ae
from OEContinuousUtils.OEContinuousUtils import (get_header_string, write_continuous)
from OEContinuousUtils.OpenEphys import (loadContinuous,)
test_files_dir = '/Users/fpbatta/dataLisa/rat27_plusmaze_base_II_2016-03-24_14-10-08/'


class TestWrite(unittest.TestCase):
    def test_write(self):
        file_in = os.path.join(test_files_dir, '100_CH9.continuous')
        file_out = os.path.join(test_files_dir, 'write_test')
        channel_data = loadContinuous(file_in, dtype=np.int16, trim_last_record=False)
        hs = get_header_string(file_in)
        write_continuous(file_out, [channel_data, ], hs)
        self.assertTrue(filecmp.cmp(file_in, file_out))

    def test_concat(self):
        file_in = os.path.join(test_files_dir, '100_CH9.continuous')
        file_in_2 = os.path.join(test_files_dir, '100_CH9_2.continuous')
        file_out = os.path.join(test_files_dir, 'write_test')
        ch_data = loadContinuous(file_in, dtype=np.int16, trim_last_record=False)
        ch_data_2 = loadContinuous(file_in_2, dtype=np.int16, trim_last_record=False)
        hs = get_header_string(file_in)
        write_continuous(file_out, (ch_data, ch_data_2), hs)
        ch_data_out = loadContinuous(file_out, dtype=np.int16, trim_last_record=False)
        ae(np.concatenate((ch_data['timestamps'], ch_data_2['timestamps'])), ch_data_out['timestamps'])

if __name__ == '__main__':
    unittest.main()
