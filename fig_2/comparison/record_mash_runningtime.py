import os
import time

working_dir = "/scratch/mbr5797/compare_fmh_simka_mash/data/hmp_gut/wgs"
filesize_to_filename = {
    1: working_dir + '/f2856_ihmp_IBD_PSM6XBTZ_P.fastq.gz',
    2: working_dir + '/f1072_ihmp_IBD_MSM5FZ9X_P.fastq.gz',
    3: working_dir + '/f1001_ihmp_IBD_ESM5MEE2_P.fastq.gz',
    4: working_dir + '/f1212_ihmp_IBD_CSM5FZ4E_P.fastq.gz',
    5: working_dir + '/f1253_ihmp_IBD_MSM5LLI8_P.fastq.gz'
}

num_readings = 5

f = open("mash_runtime.csv", "w")
f.write("filesize,avg_runtime,std_runtime\n")
for filesize, filename in filesize_to_filename.items():
    print(filename)

    # Run sourmash sketch, and record the time
    # command: sourmash sketch dna <filename> -p k=21,scaled=1000 -o <output_filename>
    time_needed_mash = []
    for _ in range(num_readings):
        start_time = time.time()
        os.system(f"mash sketch -s 1000 -k 21 {filename}")
        end_time = time.time()
        time_needed_mash.append(end_time - start_time)

    # exclude the min and the max time
    _ = time_needed_mash.sort()
    time_needed_mash = time_needed_mash[1:-1]

    avg_mash_time = 1.0 * sum(time_needed_mash) / len(time_needed_mash)
    std_mash_time = (sum([(t - avg_mash_time) ** 2 for t in time_needed_mash]) / len(time_needed_mash)) ** 0.5
    
    f.write(f"{filesize},{avg_mash_time},{std_mash_time}\n")
    f.flush()
    print(f"filesize: {filesize}, avg_sourmash_time: {avg_mash_time}, std_sourmash_time: {std_mash_time}")
f.close()

        