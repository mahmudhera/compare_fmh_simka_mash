"""
Code for unit testing
"""

import unittest

from read_fmh_sketch import read_fmh_sig_file

class TestReadFmhSigFile(unittest.TestCase):
    def test_read_fmh_sig_file(self):
        # test case 1: file does not exist
        with self.assertRaises(FileNotFoundError):
            read_fmh_sig_file('non_existent_file.sig', 21, 42, 1000)
        
        # following files: created using frac kmc and sourmash respectively, k = 21, scaled = 1000, seed = 42
        existing_file1 = '../data/toy/test1_fk_with_abund'
        existing_file2 = '../data/toy/test1_sm_with_abund'

        # test case 3: incorrect ksizze
        with self.assertRaises(ValueError):
            read_fmh_sig_file(existing_file1, 20, 42, 1000)

        # test case 4: incorrect seed
        with self.assertRaises(ValueError):
            read_fmh_sig_file(existing_file1, 21, 43, 1000)

        # test case 5: incorrect max_hash
        with self.assertRaises(ValueError):
            read_fmh_sig_file(existing_file1, 21, 42, 1001)

        # test case 6: existing file1 and file2 should have the same mins
        sigs1 = read_fmh_sig_file(existing_file1, 21, 42, 1000)
        sigs2 = read_fmh_sig_file(existing_file2, 21, 42, 1000)

        self.assertEqual(list(sigs1), list(sigs2))

        # test case 7: repeat test case 6 with no abund file
        existing_file1 = '../data/toy/test2_fk_no_abund'
        existing_file2 = '../data/toy/test2_sm_no_abund'

        sigs1 = read_fmh_sig_file(existing_file1, 21, 42, 1000)
        sigs2 = read_fmh_sig_file(existing_file2, 21, 42, 1000)

        self.assertEqual(list(sigs1), list(sigs2))





if __name__ == '__main__':
    unittest.main()