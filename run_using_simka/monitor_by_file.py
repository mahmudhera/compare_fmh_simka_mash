"""
monitor resource usages of proceses using psutil
"""
import psutil
import os
import time

def get_user_name():
    return 'mbr5797'

def get_list_of_processes():
    return psutil.process_iter()

def main(file_to_monitor, output_file):
    
    print('**********************************')
    print('STARTING MONITOR SCRIPT')
    print('**********************************')

    # stats to record
    peak_memory_stage1 = 0.0
    total_cpu_time_stage1 = 0.0

    peak_memory_stage2 = 0.0
    total_cpu_time_stage2 = 0.0

    stage1 = True
    stage2 = False

    time_to_sleep = 0.03

    last_time_monitored = time.time()

    walltime_start = time.time()

    # monitor until the file gets created
    while True:
        if os.path.exists(file_to_monitor):
            break

        time.sleep(time_to_sleep)

        try:
            # get list of processes    
            processes = get_list_of_processes()

            # turn iterator into list
            processes = list(processes)
            processes_to_benchmark = []

            for process in processes:
                # if simka is in the name of the process, track it
                if 'simka' in str(process.name()).lower():
                    processes_to_benchmark.append(process)

                if get_user_name() in process.username():
                    processes_to_benchmark.append(process)

                if 'simkamerge' in str(process.name()).lower():
                    if stage1:
                        print('*****************************')
                        print('Stage1 completed')
                        print('*****************************')

                        stage1 = False
                        stage2 = True
                        time_to_sleep = 0.01
                        time_snapshot = time.time()

            current_recorded_memory = 0.0
            current_recorded_cpu_percentage = 0.0
            for process in processes_to_benchmark:
                current_recorded_memory += process.memory_info().rss
                current_recorded_cpu_percentage += process.cpu_percent()

            delta_time = time.time() - last_time_monitored

            if stage1:
                peak_memory_stage1 = max(peak_memory_stage1, current_recorded_memory)
                total_cpu_time_stage1 += current_recorded_cpu_percentage * delta_time / 100.0

            if stage2:
                peak_memory_stage2 = max(peak_memory_stage2, current_recorded_memory)
                total_cpu_time_stage2 += current_recorded_cpu_percentage * delta_time / 100.0

            # show how many processes are being monitored
            print(f"Monitoring {len(processes_to_benchmark)} processes: {processes_to_benchmark[0].name()} .. {processes_to_benchmark[-1].name()}\r", end="")
            
            # show running process names in a single line
            #print("Running processes:", end=' ')
            #for process in processes_to_benchmark:
            #    print(process.name(), end=' ')
            #print()
        
        except psutil.NoSuchProcess:
            continue

        last_time_monitored = time.time()
        

    walltime_end = time.time()

    if stage1:
        time_snapshot = walltime_end

    # write the stats to the output file
    with open(output_file, 'w') as f:
        f.write('Stage1:\n')
        f.write(f'Peak memory usage (bytes): {peak_memory_stage1}\n')
        f.write(f'Total CPU time (seconds): {total_cpu_time_stage1}\n')
        f.write(f'Walltime (seconds): {time_snapshot - walltime_start}\n')
        f.write('\n')

        if stage2:
            f.write('Stage2:\n')
            f.write(f'Peak memory usage (bytes): {peak_memory_stage2}\n')
            f.write(f'Total CPU time (seconds): {total_cpu_time_stage2}\n')
            f.write(f'Walltime (seconds): {walltime_end - time_snapshot}\n')
            f.write('\n')

    print('**********************************')
    print('EXITING MONITOR SCRIPT')
    print('**********************************')



if __name__ == "__main__":
    # the first command line argument is the target filename
    # the second command line argument is the output filename
    # e.g. python main.py target_filename resources
    # if no pid is provided, the script will exit
    if len(os.sys.argv) < 3:
        os.sys.exit(1)

    # check first argument is a valid string
    try:
        str(os.sys.argv[1])
    except ValueError:
        os.sys.exit(1)

    # check second argument is a valid string
    try:
        str(os.sys.argv[2])
    except ValueError:
        os.sys.exit(1)

    # check if the target file already exists
    if os.path.exists(os.sys.argv[1]):
        print(f"Target file {os.sys.argv[1]} already there! Delete it first.")
        raise ValueError(f"Target file {os.sys.argv[1]} already there! Delete it first.")

    file_to_monitor = str(os.sys.argv[1])
    output_file = str(os.sys.argv[2])
    main(file_to_monitor, output_file)