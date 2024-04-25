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
    parser.add_argument('-r', '--resources', type=str, help='Resource file name', default='resources.txt')
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
            file_path = line.strip()
            sample_name = os.path.basename(file_path)
            out.write(f'{sample_name}: {file_path}\n')

    return simka_filelist

def run_simka(input_file, ksize, output_directory, temp_dir_name = './simka_temp_dir'):
    # create a filelist for simka
    simka_filelist = create_filelist_for_simka(input_file)

    # run simka
    os.system(f'simka -in {simka_filelist} -kmer-size {ksize} -out {output_directory} -out-tmp {temp_dir_name}')



def start_monitor(resource_filename):
    # start monitoring the processes
    pid = os.getpid()

    # find the directory in which this running script is present
    script_dir = os.path.dirname(os.path.realpath(__file__))

    # generate the monitoring script path: script_dir/monitor.sh
    monitoring_script_path = os.path.join(script_dir, 'monitor.py')

    os.system(f"python {monitoring_script_path} {pid} {resource_filename}&")



def main():
    args = parse_arguments()
    check_input_files_exist(args.input_file)
    start_monitor(args.resources)
    run_simka(args.input_file, args.ksize, args.output_directory)



if __name__ == '__main__':
    main()