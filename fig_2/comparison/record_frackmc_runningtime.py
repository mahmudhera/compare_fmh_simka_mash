import os
import time
import numpy as np

working_dir = "/scratch/mbr5797/compare_fmh_simka_mash/data/hmp_gut/wgs"
filesize_to_filename = {
    1: working_dir + '/f2856_ihmp_IBD_PSM6XBTZ_P.fastq.gz',
    2: working_dir + '/f1072_ihmp_IBD_MSM5FZ9X_P.fastq.gz',
    3: working_dir + '/f1001_ihmp_IBD_ESM5MEE2_P.fastq.gz',
    4: working_dir + '/f1212_ihmp_IBD_CSM5FZ4E_P.fastq.gz',
    5: working_dir + '/f1253_ihmp_IBD_MSM5LLI8_P.fastq.gz'
}

num_readings = 5

f = open("frackmc_one_thread_runtime.csv", "w")
f.write("filesize,avg_runtime,std_runtime\n")
for filesize, filename in filesize_to_filename.items():
    print(filename)

    # Run frackmc sketch, and record the time
    time_needed_frackmc_one_thread = []
    for _ in range(num_readings):
        start_time = time.time()
        os.system(f"fracKmcSketch {filename} -o {filename}.frackmc --ksize 21 --scaled 1000 --fq --n 1")
        end_time = time.time()
        time_needed_frackmc_one_thread.append(end_time - start_time)

    # exclude the min and the max time
    _ = time_needed_frackmc_one_thread.sort()
    time_needed_frackmc_one_thread = time_needed_frackmc_one_thread[1:-1]

    avg_frackmc_time = np.mean(time_needed_frackmc_one_thread)
    std_frackmc_time = np.std(time_needed_frackmc_one_thread)
    
    f.write(f"{filesize},{avg_frackmc_time},{std_frackmc_time}\n")
    f.flush()
    print(f"filesize: {filesize}, avg_frackmc_time: {avg_frackmc_time}, std_frackmc_time: {std_frackmc_time}")

f.close()


f = open("frackmc_many_threads_runtime.csv", "w")
f.write("filesize,avg_runtime,std_runtime\n")
for filesize, filename in filesize_to_filename.items():
    print(filename)

    # Run frackmc sketch, and record the time
    time_needed_frackmc_one_thread = []
    for _ in range(num_readings):
        start_time = time.time()
        os.system(f"fracKmcSketch {filename} -o {filename}.frackmc --ksize 21 --scaled 1000 --fq --n 32")
        end_time = time.time()
        time_needed_frackmc_one_thread.append(end_time - start_time)

    # exclude the min and the max time
    _ = time_needed_frackmc_one_thread.sort()
    time_needed_frackmc_one_thread = time_needed_frackmc_one_thread[1:-1]

    avg_frackmc_time = np.mean(time_needed_frackmc_one_thread)
    std_frackmc_time = np.std(time_needed_frackmc_one_thread)
    
    f.write(f"{filesize},{avg_frackmc_time},{std_frackmc_time}\n")
    f.flush()
    print(f"filesize: {filesize}, avg_frackmc_time: {avg_frackmc_time}, std_frackmc_time: {std_frackmc_time}")

f.close()

        