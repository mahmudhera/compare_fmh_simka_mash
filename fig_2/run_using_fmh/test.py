"""
Code for unit testing
"""

import unittest
import random

from read_fmh_sketch import read_fmh_sig_file
from run_by_fmh_wrapper import count_num_common
from run_by_fmh_wrapper import compute_magnitute
from run_by_fmh_wrapper import get_dot_product
from run_by_fmh_wrapper import compute_metric_for_a_pair

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

class TestCountNumCommon(unittest.TestCase):
    def test1(self):
        # test case 1: no common mins
        list1 = [1, 2, 3]
        list2 = [4, 5, 6]

        self.assertEqual(count_num_common(list1, list2), 0)

    def test2(self):
        # test case 2: all common mins
        list1 = [1, 2, 3]
        list2 = [1, 2, 3]

        self.assertEqual(count_num_common(list1, list2), 3)

    def test3(self):
        # test case 3: some common mins
        list1 = [1, 2, 3]
        list2 = [2, 3, 4]

        self.assertEqual(count_num_common(list1, list2), 2)

    def test4(self):
        # repeat test1 with randomly generated lists
        # create list1 with 10000 elements, sorted
        list1 = list(range(10000))
        # create list2 with 10000 elements, sorted
        list2 = list(range(10001, 25000))

        self.assertEqual(count_num_common(list1, list2), 0)
        self.assertEqual(count_num_common(list2, list1), 0)

    def test5(self):
        list1 = list(range(10000))
        list2 = list(range(10000))

        self.assertEqual(count_num_common(list1, list2), 10000)

    def test6(self):
        list1 = list(range(10000))
        list2 = list(range(5000, 12000))

        self.assertEqual(count_num_common(list1, list2), 5000)

class TestComputeMagnitute(unittest.TestCase):
    def test1(self):
        # test case 1: empty list
        self.assertEqual(compute_magnitute([]), 0)

    def test2(self):
        # test case 2: list with one element
        self.assertEqual(compute_magnitute([(1, 1)]), 1)

    def test3(self):
        # test case 3: sig with single element, varying abundances
        
        # create a list of random positive integers
        abundances = [random.randint(1, 100) for i in range(100)]
        for abund in abundances:
            self.assertAlmostEqual(compute_magnitute([(1, abund)]), abund)

    def test4(self):
        # test case 4: sig with multiple elements, all with 1 abundance
        num_runs = 100
        for i in range(num_runs):
            num_elements = random.randint(1, 1000)
            sig = [(i, 1) for i in range(num_elements)]
            self.assertAlmostEqual(compute_magnitute(sig), num_elements**0.5)

            sig = [(i, 5) for i in range(num_elements)]
            self.assertAlmostEqual(compute_magnitute(sig), 5 * num_elements**0.5)

class TestGetDotProduct(unittest.TestCase):
    def test1(self):
        # test case 1: empty lists
        self.assertEqual(get_dot_product([], []), 0)

    def test2(self):
        # test case 2: one empty list
        self.assertEqual(get_dot_product([(1, 1)], []), 0)
        self.assertEqual(get_dot_product([], [(1, 1)]), 0)

    def test3(self):
        # test case 3: one element in each list, no common mins
        self.assertEqual(get_dot_product([(1, 1)], [(2, 1)]), 0)

    def test4(self):
        # test case 4: one element in each list, common min
        self.assertEqual(get_dot_product([(1, 1)], [(1, 1)]), 1)

    def test5(self):
        # test case 5: multiple elements in each list, no common mins
        self.assertEqual(get_dot_product([(1, 1), (2, 1), (3, 1)], [(4, 1), (5, 1), (6, 1)]), 0)

    def test6(self):
        # test case 6: multiple elements in each list, all common mins
        self.assertEqual(get_dot_product([(1, 1), (2, 1), (3, 1)], [(1, 1), (2, 1), (3, 1)]), 3)

    def test7(self):
        # test case 7: many common elements, all abudances are random
        num_elements_set_1 = 1000
        num_elements_set_2 = 2000
        num_common_elements = 750

        sig1 = []
        sig2 = []

        dot_product = 0.0
        for i in range(num_elements_set_1):
            # flip a coin to decide if this element is common
            random_float = random.random()
            threshold = num_common_elements / num_elements_set_1
            if random_float < threshold:
                abund1, abund2 = random.randint(1, 100), random.randint(1, 100)
                sig1.append((i, abund1))
                sig2.append((i, abund2))
                dot_product += abund1 * abund2

            else:
                sig1.append((i, 1))

        num_elements_in_set_2 = len(sig2)
        more_to_insert = num_elements_set_2 - num_elements_in_set_2
        for i in range(num_elements_set_1, num_elements_set_1+more_to_insert):
            abund = random.randint(1, 100)
            sig2.append((i, abund))

        self.assertAlmostEqual(get_dot_product(sig1, sig2), dot_product)

    def test8(self):
        # test case 8: repeat test case 7, but with all abundances as 1
        num_elements_set_1 = 1000
        num_elements_set_2 = 2000
        num_common_elements = 750

        sig1 = []
        sig2 = []

        dot_product = 0.0
        for i in range(num_elements_set_1):
            # flip a coin to decide if this element is common
            random_float = random.random()
            threshold = num_common_elements / num_elements_set_1
            if random_float < threshold:
                sig1.append((i, 1))
                sig2.append((i, 1))
                dot_product += 1

            else:
                sig1.append((i, 1))

        num_elements_in_set_2 = len(sig2)
        more_to_insert = num_elements_set_2 - num_elements_in_set_2

        for i in range(num_elements_set_1, num_elements_set_1+more_to_insert):
            sig2.append((i, 1))

        self.assertAlmostEqual(get_dot_product(sig1, sig2), dot_product)

class TestComputeMetricForAPair(unittest.TestCase):
    def test1(self):
        # test case 1: empty sigs
        ret_list = [-1]
        index = 0
        compute_metric_for_a_pair([], [], 'cosine', ret_list, index)
        self.assertEqual(ret_list[index], 0)

    def test2(self):
        # test case 2: one empty sig
        ret_list = [-1]
        index = 0
        compute_metric_for_a_pair([], [(1, 1)], 'cosine', ret_list, index)
        self.assertEqual(ret_list[index], 0)

        compute_metric_for_a_pair([(1, 1)], [], 'cosine', ret_list, index)
        self.assertEqual(ret_list[index], 0)

    def test3(self):
        # test case 7: many common elements, all abudances are random
        num_elements_set_1 = 1000
        num_elements_set_2 = 2000
        num_common_elements = 750

        sig1 = []
        sig2 = []

        dot_product = 0.0
        for i in range(num_elements_set_1):
            # flip a coin to decide if this element is common
            random_float = random.random()
            threshold = num_common_elements / num_elements_set_1
            if random_float < threshold:
                abund1, abund2 = random.randint(1, 100), random.randint(1, 100)
                sig1.append((i, abund1))
                sig2.append((i, abund2))
                dot_product += abund1 * abund2

            else:
                sig1.append((i, 1))

        num_elements_in_set_2 = len(sig2)
        more_to_insert = num_elements_set_2 - num_elements_in_set_2
        for i in range(num_elements_set_1, num_elements_set_1+more_to_insert):
            abund = random.randint(1, 100)
            sig2.append((i, abund))

        ret_list = [-1]
        index = 0
        compute_metric_for_a_pair(sig1, sig2, 'cosine', ret_list, index)
        self.assertAlmostEqual(ret_list[index], dot_product / (compute_magnitute(sig1) * compute_magnitute(sig2)))


if __name__ == '__main__':
    unittest.main()