"""
In this script, we will compare the outputs of various methods.
"""

import numpy as np
import argparse
import pandas as pd

def parse_args():
    # list of arguments:
    # 1. path to fmh output file that has cosine similarity values
    # 2. path to simka output file that has Chord distance values

    parser = argparse.ArgumentParser(description="Compare outputs of different methods")
    parser.add_argument("fmh_output", type=str, help="Path to FMH output file")
    parser.add_argument("mash_output", type=str, help="Path to Mash output file")
    parser.add_argument("gt_output", type=str, help="Path to ground truth output file")

    return parser.parse_args()

def read_output(fmh_output):
    """
    Read the FMH output file and return the cosine similarity values indexed by proper pairs
    """
    # use whitespaces as separator
    df = pd.read_csv(fmh_output, header=None, delim_whitespace=True)
    df.columns = ["file1", "file2", "cosine_similarity"]

    # iterate over all rows
    pair_to_cosine = {}
    for _, row in df.iterrows():
        filename1 = row["file1"]
        filename1 = filename1.split("/")[-1]
        filename2 = row["file2"]
        filename2 = filename2.split("/")[-1]
        pair_to_cosine[(filename1, filename2)] = row["cosine_similarity"]
        pair_to_cosine[(filename2, filename1)] = row["cosine_similarity"]

    return pair_to_cosine

def compare_outputs(fmh_output, mash_output, gt_output):
    """
    Compare the outputs of FMH and Simka
    """
    pairs_to_cosine_fmh = read_output(fmh_output)
    pairs_to_cosine_mash = read_output(mash_output)
    pairs_to_cosine_gt = read_output(gt_output)

    # iterate over all pairs and compare the values
    print('fmh_error, mash_error, gt, fmh, mash')
    for pair in pairs_to_cosine_fmh:
        try:
            cosine_fmh = pairs_to_cosine_fmh[pair]
            cosine_mash = pairs_to_cosine_mash[pair]
            cosine_gt = pairs_to_cosine_gt[pair]
        except KeyError:
            continue

        # continue if any of these < 0
        if cosine_fmh < 0 or cosine_mash < 0 or cosine_gt < 0:
            continue

        # print: cosine_fmh-cosine_gt, cosine_mash-cosine_gt
        print(cosine_fmh - cosine_gt, cosine_mash - cosine_gt, cosine_gt, cosine_fmh, cosine_mash)


if __name__ == "__main__":
    args = parse_args()
    compare_outputs(args.fmh_output, args.mash_output, args.gt_output)