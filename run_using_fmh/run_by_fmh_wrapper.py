"""
This script will take the following inputs:
1. The path to a file that contains absolute path of the input files (files can be fasta, fastq, gz etc.)
1. The kmer size (default: 21)
1. The scale factor (scaled value)
1. The metric to compute (e.g. 'cosine', 'braycurtis', 'canberra', 'jaccard', 'kulsinski')
1. The number of cores to use
1. The output file name

The script will then do the following:
1. For all the input files, it will generate FMH sketch files
1. Using the sketches, the script will then compute pairwise metric values
1. The previous step will be parallelized using the number of cores specified
"""


# Requirements
# FracKmc needs to be in the PATH
# Download all binaries of FracKmc, and then add the path to the binaries to the PATH

# Usage
# python run_by_fmh_wrapper.py -i <input_file> -s <scale_factor> -m <metric> -w <weighted> -c <cores> -o <output_file>

import argparse
import os
import subprocess
import multiprocessing

from read_fmh_sketch import read_fmh_sig_file


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run FMH to compute metrics on input files')
    parser.add_argument('-i', '--input_file', type=str, help='Path to file containing input files')
    parser.add_argument('-k', '--ksize', type=int, help='Kmer size', default=21)
    parser.add_argument('-s', '--scale_factor', type=int, help='Scale factor', default=1000)
    parser.add_argument('-m', '--metric', type=str, help='Metric to compute', default='cosine')
    parser.add_argument('-c', '--cores', type=int, help='Number of cores', default=128)
    parser.add_argument('-o', '--output_file', type=str, help='Output file name')
    # add seed as an argument
    parser.add_argument('-S', '--seed', type=int, help='Seed', default=42)
    args = parser.parse_args()
    return args


def check_input_files_exist(input_file):
    # first check that the input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f'Input file {input_file} does not exist')

    # next, check that all the files in the input file exist
    with open(input_file, 'r') as f:
        for line in f:
            if not os.path.exists(line.strip()):
                raise FileNotFoundError(f'File {line.strip()} does not exist')


def check_num_cores(cores):
    if cores < 1:
        raise ValueError('Number of cores should be greater than 0')
    
    # check that the machine has enough cores
    num_cores = multiprocessing.cpu_count()
    if cores > num_cores:
        raise ValueError(f'Machine does not have enough cores. Number of cores requested: {cores}, Number of cores available: {num_cores}')


def generate_fmh_sketch(file, scale_factor, ksize, output_file, is_fasta, seed=42):
    # use the proper command
    # command: fracKmcSketch <input_filename> <sketch_filename> --ksize <ksize> --scaled <scaled> --seed 42 --fa/--fq
    if is_fasta:
        cmd = f'fracKmcSketch {file} {output_file} --ksize {ksize} --scaled {scale_factor} --seed {seed} --fa'
    else:
        cmd = f'fracKmcSketch {file} {output_file} --ksize {ksize} --scaled {scale_factor} --seed {seed} --fq'

    # run the command and check for errors
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise Exception(f'Error while generating sketch for file {file}: {e}')


"""
list1 and list2 are sorted lists of integers
This function should return the number of common elements between the two lists
"""
def count_num_common(list1, list2):
    
    # check if either of the lists is empty
    if len(list1) == 0 or len(list2) == 0:
        return 0
    
    # use merge sort like operation to find the common elements
    i = 0
    j = 0
    count = 0

    while i < len(list1) and j < len(list2):
        if list1[i] == list2[j]:
            count += 1
            i += 1
            j += 1
        elif list1[i] < list2[j]:
            i += 1
        else:
            j += 1

    return count


def compute_metric_for_a_pair(sig1, sig2, metric):
    if metric == 'cosine':
        # compute the dot product
        dot_product = count_num_common(sig1, sig2)
        
        # compute the magnitudes
        magnitude1 = len(sig1)
        magnitude2 = len(sig2)
        
        # compute the cosine similarity
        return dot_product / (magnitude1**0.5 * magnitude2**0.5)


def main():
    args = parse_arguments()
    check_input_files_exist(args.input_file)
    check_num_cores(args.cores)
    
    # read the input file
    input_files = []
    with open(args.input_file, 'r') as f:
        for line in f:
            input_files.append(line.strip())
    
    # generate sketches
    sketch_files = []
    for file in input_files:
        # sketch filename format: <input_filename>_ksize_scaled_seed.sig
        sketch_filename = f'{file}_{args.ksize}_{args.scale_factor}_{args.seed}.sig'
        generate_fmh_sketch(file, args.scale_factor, args.ksize, sketch_filename, file.endswith('.fa') or file.endswith('.fasta'), args.seed)
        sketch_files.append(sketch_filename)

    # read in all signatures
    filename_to_sig_dict = {}
    for sketch_file in sketch_files:
        sigs = read_fmh_sig_file(sketch_file, args.ksize, args.seed, args.scale_factor)
        filename_to_sig_dict[sketch_file] = sigs

    # compute pairwise metrics
    pair_to_metric_dict = {}
    print('Computing pairwise metrics')
    for i in range(len(input_files)):
        for j in range(i+1, len(input_files)):
            sig1 = filename_to_sig_dict[input_files[i]]
            sig2 = filename_to_sig_dict[input_files[j]]
            metric = compute_metric_for_a_pair(sig1, sig2, args.metric)
            pair_to_metric_dict[(input_files[i], input_files[j])] = metric

    # write the output to a file
    with open(args.output_file, 'w') as f:
        for pair, metric in pair_to_metric_dict.items():
            f.write(f'{pair[0]}\t{pair[1]}\t{metric}\n')
                
    print('Done')