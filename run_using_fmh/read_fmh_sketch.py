"""
This script reads a FracMinHash sketch file
"""

import os
import json
import argparse
import numpy as np

"""
The current version assumes noabund
TODO: Add support for abund
"""
def read_fmh_sig_file(file, ksize, seed, scaled):
    # compute the correct max_hash
    theoretical_max_hash = np.longdouble(2**64 - 1)
    divide_by = np.longdouble(scaled)
    target_max_hash = round( theoretical_max_hash / divide_by)

    # first check that the input file exists
    if not os.path.exists(file):
        raise FileNotFoundError(f'Input file {file} does not exist')

    # read the file as json
    try:
        f = open(file, 'r')
        json_data = json.load(f)
        f.close()
    except json.JSONDecodeError as e:
        raise Exception(f'Error while reading the file {file}: {e}')
    
    json_data = json_data[0]
        
    # check that the json data has the required keys
    required_keys = ['signatures']
    if not all(key in json_data for key in required_keys):
        raise KeyError(f'File {file} does not have the required keys: {required_keys}')
        
    # check that the signatures are a list
    if not isinstance(json_data['signatures'], list):
        raise TypeError(f'Signatures in file {file} should be a list')
    
    # check that each entry in the signatures is a dictionary containing the following keys:
    # 'ksize': the kmer size, an integer
    # 'seed': the seed used to generate the sketch, an integer
    # 'max_hash': the maximum hash value, an integer
    # 'mins': a list of integers

    sigs = json_data['signatures']
    for sig in sigs:
        required_keys = ['ksize', 'seed', 'max_hash', 'mins']
        if not all(key in sig for key in required_keys):
            raise KeyError(f'Signature {sig} does not have the required keys: {required_keys}')
        
        # check that the values are of the correct type
        if not isinstance(sig['ksize'], int):
            raise TypeError(f'ksize in signature {sig} should be an integer')
        if not isinstance(sig['seed'], int):
            raise TypeError(f'seed in signature {sig} should be an integer')
        if not isinstance(sig['max_hash'], int):
            raise TypeError(f'max_hash in signature {sig} should be an integer')
        if not isinstance(sig['mins'], list):
            raise TypeError(f'mins in signature {sig} should be a list')

        # if this signature is the correct ksize, and correct seed, and correct max_hash, return the mins
        if sig['ksize'] == ksize and sig['seed'] == seed and sig['max_hash'] == target_max_hash:
            # if "abundances" is present, extract the abundances
            if 'abundances' in sig:
                return zip(sig['mins'], sig['abundances'])
            else:
                return zip(sig['mins'], [1.0] * len(sig['mins']))
        
    # if we reach this point, we did not find the correct signature
    raise ValueError(f'Could not find the signature with ksize={ksize}, seed={seed}, and max_hash={target_max_hash}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Read a FracMinHash sketch file')
    parser.add_argument('-f', '--file', type=str, help='Path to the FracMinHash sketch file')
    parser.add_argument('-k', '--ksize', type=int, help='Kmer size', default=21)
    parser.add_argument('-s', '--seed', type=int, help='Seed used to generate the sketch', default=42)
    parser.add_argument('--scaled', type=int, help='Scale factor used to generate the sketch', default=1000)
    args = parser.parse_args()
    
    mins = read_fmh_sig_file(args.file, args.ksize, args.seed, args.scaled)
    print('First 10 hash values:')
    print(mins[:10])

    print('Last 10 hash values:')
    print(mins[-10:])
