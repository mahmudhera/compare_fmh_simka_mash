"""
In this script, we will run mash to compute the results.
"""

import os
import argparse
import json
import multiprocessing



def process_a_range_of_pairs(filenames, filenames_to_hashes, all_i_j_pairs, start_index, end_index, return_list):
    """
    Compute the pairwise cosines for a range of pairs of files
    """
    completed = 0
    for index in range(start_index, end_index):
        i, j = all_i_j_pairs[index]
        filename1 = filenames[i]
        filename2 = filenames[j]
        hash1 = filenames_to_hashes[filename1]
        hash2 = filenames_to_hashes[filename2]
        
        dot_product = set(hash1).intersection(hash2)
        cosine = len(dot_product) / (len(hash1)**0.5 * len(hash2)**0.5)
        return_list[index] = cosine

        completed += 1
        print(f"Completed {completed} out of {end_index - start_index}", end='\r')


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
    parser.add_argument('--no_parallel', dest='no_parallel', action='store_true', help='Do not parallelize')
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

    if args.no_parallel:
        pair_to_metric_dict = {}
        num_completed = 0
        total = len(files) * (len(files) - 1) // 2
        for i in range(len(files)):
            for j in range(i+1, len(files)):
                filename1 = files[i]
                filename2 = files[j]
                hash1 = filenames_to_hashes[filename1]
                hash2 = filenames_to_hashes[filename2]
                
                dot_product = set(hash1).intersection(hash2)
                cosine = len(dot_product) / (len(hash1)**0.5 * len(hash2)**0.5)
                pair_to_metric_dict[(filename1, filename2)] = cosine
                num_completed += 1
                print(f"Completed {num_completed} out of {total}", end='\r')
        print()
        print('*****************************')
        print('Computing completed, writing to file')
        print('*****************************')

        # write the results to the output file
        with open(args.output_file, "w") as f:
            f.write("file1,file2,cosine_similarity\n")
            for (filename1, filename2), cosine in pair_to_metric_dict.items():
                f.write(f"{filename1},{filename2},{cosine}\n")
                

    num_threads = 128
    all_i_j_pairs = []
    for i in range(len(files)):
        for j in range(i+1, len(files)):
            all_i_j_pairs.append((i, j))

    # create a list using multiprocessing manager
    # this list will be shared among all processes
    return_list = multiprocessing.Manager().list([-1] * len(all_i_j_pairs))

    list_processes = []
    for i in range(num_threads):
        start_index = i * len(all_i_j_pairs) // num_threads
        end_index = (i + 1) * len(all_i_j_pairs) // num_threads
        if i == num_threads - 1:
            end_index = len(all_i_j_pairs)
        p = multiprocessing.Process(target=process_a_range_of_pairs, args=(files, filenames_to_hashes, all_i_j_pairs, start_index, end_index, return_list))
        p.start()
        list_processes.append(p)

    for p in list_processes:
        p.join()

    print('*****************************')
    print('Computing completed, writing to file')
    print('*****************************')

    # write the results to the output file
    index = 0
    with open(args.output_file, "w") as f:
        f.write("file1,file2,cosine_similarity\n")
        for i in range(len(files)):
            for j in range(i+1, len(files)):
                cosine = return_list[index]
                index += 1
                f.write(f"{files[i]},{files[j]},{cosine}\n")



if __name__ == "__main__":
    main()