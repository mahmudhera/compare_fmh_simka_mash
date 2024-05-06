"""
This script generates the dataset for the simulated experiment.
We take two fastq files and the number of desired files as input and generate that many files.
We will divide 0 to 1 in n parts, use those values as weights.
We will use weight many reads from one file, and (1-weight) many reads from the other file.
"""

import argparse
import os
import gzip

def parse_args():
    """
    Parse the arguments
    """
    parser = argparse.ArgumentParser(description="Generate dataset for simulated experiment")
    parser.add_argument("fastq1", type=str, help="Path to the first fastq file")
    parser.add_argument("fastq2", type=str, help="Path to the second fastq file")
    parser.add_argument("num_files", type=int, help="Number of files to generate")
    return parser.parse_args()

def get_num_lines_in_file(filename):
    if filename.endswith(".gz"):
        with gzip.open(filename, "rt") as f:
            return sum(1 for _ in f)
    else:
        with open(filename) as f:
            return sum(1 for _ in f)
        
def main():
    args = parse_args()
    n1 = get_num_lines_in_file(args.fastq1)
    n2 = get_num_lines_in_file(args.fastq2)

    # get the weights
    weights = [i/args.num_files for i in range(1,args.num_files)]
    for weight in weights:
        lines_to_get_from_file1 = int(n1/4 * weight) * 4
        lines_to_get_from_file2 = int(n2/4 * (1-weight)) * 4

        # use cat and head to get the first n lines
        os.system(f"cat {args.fastq1} | head -n {lines_to_get_from_file1} > file1.fastq")
        os.system(f"cat {args.fastq2} | head -n {lines_to_get_from_file2} > file2.fastq")
        os.system(f"cat file1.fastq file2.fastq > file_{weight}.fastq")
        os.system(f"rm file1.fastq file2.fastq")

if __name__ == "__main__":
    main()