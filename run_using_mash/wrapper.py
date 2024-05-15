"""
In this script, we will run mash to compute the results.
"""

import os
import argparse
import json

"""
arguments:
1. file list that contains many files
2. output file name
3. kmer size (default 21)
4. sketch size (default 10000)
"""
def parse_args():
    parser = argparse.ArgumentParser(description="Run Mash")
    parser.add_argument("file_list", type=str, help="Path to the file list")
    parser.add_argument("output_file", type=str, help="Path to the output file")
    parser.add_argument("--kmer_size", type=int, default=21, help="Kmer size")
    parser.add_argument("--sketch_size", type=int, default=10000, help="Sketch size")
    parser.add_argument("--num_cores", type=int, default=128, help="Num of cores to parallelize over")
    return parser.parse_args()

def main():
    args = parse_args()

    # ensure that no empty lines are present in the file list
    with open(args.file_list) as f:
        files = f.readlines()
        files = [file.strip() for file in files if file.strip()]

    # if there is empty line, exit with an error message
    if len(files) == 0:
        print("No files in the file list")
        return

    # ensure that all files in the file list are present
    for file in files:
        assert os.path.exists(file)
    
    print('*****************************')
    print('Running Mash')
    print('*****************************')

    # create a sketch for each file in the file list
    # command: mash sketch -k kmer_size -s sketch_size -o mash_sketch -l filelist
    # the generated output file: mash_sketch.msh
    os.system(f"mash sketch -k {args.kmer_size} -s {args.sketch_size} -o mash_sketch -l {args.file_list} -p {args.num_cores}")

    print('*****************************')
    print('Sketching completed, creating json')
    print('*****************************')

    # dump the .msh file into a json file
    # command: mash info mash_sketch.msh -d > mash_sketch.json
    os.system(f"mash info mash_sketch.msh -d > mash_sketch.json")

    print('*****************************')
    print('Json created, reading hashes')
    print('*****************************')

    # read the json file to obtain the min hash values
    # format: data['sketches']['name'] is the filename
    # data['sketches']['hashes'] is the list of the min hash values
    filenames_to_hashes = {}
    with open("mash_sketch.json") as f:
        data = json.load(f)
        for i in range( len(data['sketches']) ):
            filename = str(data['sketches'][i]['name'])
            filenames_to_hashes[filename] = list(data['sketches'][i]['hashes'])

    print('*****************************')
    print('Hashes read, computing pairwise cosines')
    print('*****************************')

    # compute pairwise cosines (no abundances, so straightforward)
    # iterate over all pairs of files
    num_completed = 0
    total_pairs = len(files) * (len(files) - 1) // 2
    with open(args.output_file, "w") as f:
        for i in range(len(files)):
            for j in range(i+1, len(files)):
                filename1 = files[i]
                filename2 = files[j]
                hash1 = filenames_to_hashes[filename1]
                hash2 = filenames_to_hashes[filename2]
                
                dot_product = set(hash1).intersection(hash2)
                cosine = len(dot_product) / (len(hash1)**0.5 * len(hash2)**0.5)
                f.write(f"{filename1}\t{filename2}\t{cosine}\n")
                num_completed += 1
                print(f"Percentage completed {100*num_completed/total_pairs}%\r", end="")
    print('')


if __name__ == "__main__":
    main()