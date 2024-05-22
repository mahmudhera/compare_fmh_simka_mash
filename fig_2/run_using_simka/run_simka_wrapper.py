"""
In this script, we will run simka
"""

import os
import argparse

# Requirements: SIMKA needs to be in the PATH variable

def parse_arguments():
    parser = argparse.ArgumentParser(description='Run simka to compute metrics on input files')
    parser.add_argument('-i', '--input_file', type=str, help='Path to file containing input files')
    parser.add_argument('-k', '--ksize', type=int, help='Kmer size', default=21)
    parser.add_argument('-o', '--output_directory', type=str, help='Output directory name')
    parser.add_argument('-r', '--resources', type=str, help='Resource file name', default=None)
    parser.add_argument('-t', '--temp_dir_name', type=str, help='Temporary directory name', default='./simka_temp_dir')
    # use argument for num threads
    parser.add_argument('-n', '--num_threads', type=int, help='Number of threads to use in simkaMerge', default=1)
    args = parser.parse_args()
    return args

def check_input_files_exist(input_file):
    # first check that the input file exists
    if not os.path.exists(input_file):
        raise FileNotFoundError(f'Input file {input_file} does not exist')

    # next, check that all the files in the input file exist
    with open(input_file, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            if line.strip() == '':
                continue
            if not os.path.exists(line.strip()):
                raise FileNotFoundError(f'File {line.strip()} does not exist')
            
"""
SIMKA required file list is not the same as FMH. In this function, we will create a filelist for SIMKA
"""
def create_filelist_for_simka(input_file):
    # our input file will have a list of files, one per line
    # what we need for simka: one line for one file in the following format:
    # <sample_name>: <file_path>
    # we will use the file name as the sample name
    # simka file name format: <input_file>_for_simka

    simka_filelist = f'{input_file}_for_simka'
    with open(input_file, 'r') as f, open(simka_filelist, 'w') as out:
        for line in f:
            if line == '\n':
                continue
            if line.strip() == '':
                continue
            
            file_path = line.strip()
            sample_name = os.path.basename(file_path)
            out.write(f'{sample_name}: {file_path}\n')

    return simka_filelist

def run_simka(input_file, ksize, output_directory, temp_dir_name = './simka_temp_dir', num_threads = 1):
    # create a filelist for simka
    simka_filelist = create_filelist_for_simka(input_file)

    # run simka
    cmd = f'simka -in {simka_filelist} -kmer-size {ksize} -out {output_directory} -out-tmp {temp_dir_name} -max-merge {num_threads}'
    print(cmd)
    os.system(cmd)



def start_monitor(simka_output_directory, resource_filename):
    # start monitoring the processes
    required_filename = 'mat_abundance_jaccard.csv.gz'
    required_file_path = os.path.join(simka_output_directory, required_filename)

    # find the directory in which this running script is present
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # generate the monitoring script path: script_dir/monitor.sh
    monitoring_script_path = os.path.join(script_dir, 'monitor_by_file.py')

    os.system(f"python {monitoring_script_path} {required_file_path} {resource_filename}&")



def main():
    args = parse_arguments()
    check_input_files_exist(args.input_file)
    if args.resources != None:
        start_monitor(args.output_directory, args.resources)
    run_simka(args.input_file, args.ksize, args.output_directory, args.temp_dir_name, args.num_threads)



if __name__ == '__main__':
    main()