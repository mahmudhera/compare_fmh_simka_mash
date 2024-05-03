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
    parser.add_argument("simka_output", type=str, help="Path to Simka output file")

    return parser.parse_args()

def read_fmh_output(fmh_output):
    """
    Read the FMH output file and return the cosine similarity values indexed by proper pairs
    """
    df = pd.read_csv(fmh_output, sep="\t", header=None)
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

def read_simka_output(simka_output):
    """
    Read the Simka output file and return the Chord distance values indexed by proper pairs
    """
    df = pd.read_csv(simka_output, sep=";")

    # get the first column as a list
    filenames = list(df.columns)

    # iterate over all pairs. The df is a square matrix. Header contains filenames
    pair_to_chord = {}
    for i in range(1, len(filenames)):
        for j in range(i+1, len(filenames)):
            filename1 = filenames[i]
            filename1 = filename1.split("/")[-1]
            filename2 = filenames[j]
            filename2 = filename2.split("/")[-1]
            
            pair_to_chord[(filename1, filename2)] = df.iloc[i-1, j]

    return pair_to_chord

def chord_to_cosine(chord):
    """
    Convert Chord distance to Cosine similarity
    """
    return 1.0 - 0.5 * chord**2

def compare_outputs(fmh_output, simka_output):
    """
    Compare the outputs of FMH and Simka
    """
    pair_to_cosine = read_fmh_output(fmh_output)
    pair_to_chord = read_simka_output(simka_output)

    # iterate over all pairs and compare the values
    for pair in pair_to_cosine:
        cosine_fmh = pair_to_cosine[pair]
        chord_simka = pair_to_chord[pair]
        cosine_simka = chord_to_cosine(chord_simka)

        print(f"{cosine_simka}, {cosine_fmh}, {cosine_simka - cosine_fmh}")


if __name__ == "__main__":
    args = parse_args()
    compare_outputs(args.fmh_output, args.simka_output)