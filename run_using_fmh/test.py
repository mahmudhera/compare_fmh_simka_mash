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
        
        # test case 2: file is not a valid json file
        with self.assertRaises(Exception):
            read_fmh_sig_file('test.json', 21, 42, 1000)
        
        # test case 3: file does not have the required keys
        with self.assertRaises(KeyError):
            read_fmh_sig_file('test2.json', 21, 42, 1000)
        
        # test case 4: signatures in the file is not a list
        with self.assertRaises(TypeError):
            read_fmh_sig_file('test3.json', 21, 42, 1000)
        
        # test case 5: signature does not have the required keys
        with self.assertRaises(KeyError):
            read_fmh_sig_file('test4.json', 21, 42, 1000)
        
        # test case 6: ksize in the signature is not an integer
        with self.assertRaises(TypeError):
            read_fmh_sig_file('test5.json', 21, 42, 1000)
        
        # test case 7: seed in the signature is not an integer
        with self.assertRaises(TypeError):
            read_fmh_sig_file('test6.json', 21, 42, 1000)
        
        # test case 8: max_hash in the signature is not an integer
        with self.assertRaises(TypeError):
            read_fmh_sig_file('test7.json', 21, 42, 1000)
        
        # test case 9: mins in the signature is not a list
        with self.assertRaises(TypeError):
            read_fmh_sig_file('test8.json', 21, 42, 1000)


if __name__ == '__main__':
    unittest.main()