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

def main(pid_to_monitor, output_file):
    # get user name
    user_name = get_user_name()

    # get start time of this process
    pid_this_proess = os.getpid()
    #pid_this_proess = -1
    
    # get info of process to monitor
    process_to_monitor = psutil.Process(pid_to_monitor)
    create_time_of_process_to_monitor = process_to_monitor.create_time()
    create_time_of_process_to_monitor = float(create_time_of_process_to_monitor)

    print('Monitoring process with PID:', pid_to_monitor)
    print('Process name:', process_to_monitor.name())
    print('Process create time:', create_time_of_process_to_monitor)

    # stats to record
    peak_memory = 0.0
    total_cpu_time = 0.0

    last_time_monitored = time.time()

    walltime_start = time.time()

    try:

        while process_to_monitor.is_running():
            time.sleep(0.1)

            # first check if the process is still running
            if not process_to_monitor.is_running():
                break

            # get list of processes    
            processes = get_list_of_processes()

            # turn iterator into list
            processes = list(processes)
            processes_to_benchmark = []

            for process in processes:
                # get creation time of process
                creation_time = float(process.create_time())

                if creation_time >= create_time_of_process_to_monitor and process.username() == user_name and process.pid != pid_this_proess:
                    processes_to_benchmark.append(process)

                if process.name == 'python':
                    print(process)

            current_recorded_memory = 0.0
            current_recorded_cpu_percentage = 0.0
            for process in processes_to_benchmark:
                current_recorded_memory += process.memory_info().rss
                current_recorded_cpu_percentage += process.cpu_percent()

            delta_time = time.time() - last_time_monitored
            peak_memory = max(peak_memory, current_recorded_memory)
            total_cpu_time += current_recorded_cpu_percentage * delta_time / 100.0

            #print(current_recorded_cpu_percentage)

            #print(process_to_monitor, delta_time, current_recorded_cpu_percentage, total_cpu_time)
            # show how many processes are being monitored
            print(f"Monitoring {len(processes_to_benchmark)} processes")

            # show running process names in a single line
            print("Running processes:", end=' ')
            for process in processes_to_benchmark:
                print(process.name(), end=' ')
            print()

            last_time_monitored = time.time()
    
    except psutil.NoSuchProcess:
        pass

    # continue monitoring as long as a process named 'simkaMerge' is running
    while True:
        time.sleep(0.1)

        # get list of processes
        processes = get_list_of_processes()

        # turn iterator into list
        processes = list(processes)
        processes_to_benchmark = []

        for process in processes:
            # get creation time of process
            creation_time = float(process.create_time())

            if creation_time >= create_time_of_process_to_monitor and process.username() == user_name and process.pid != pid_this_proess:
                if process.name() == 'simkaMerge':
                    processes_to_benchmark.append(process)

        if len(processes_to_benchmark) == 0:
            break

        current_recorded_memory = 0.0
        current_recorded_cpu_percentage = 0.0
        for process in processes_to_benchmark:
            current_recorded_memory += process.memory_info().rss
            current_recorded_cpu_percentage += process.cpu_percent()

        delta_time = time.time() - last_time_monitored
        peak_memory = max(peak_memory, current_recorded_memory)
        total_cpu_time += current_recorded_cpu_percentage * delta_time / 100.0

        # show how many processes are being monitored
        print(f"Monitoring {len(processes_to_benchmark)} processes")

        # show running process names in a single line
        print("Running processes:", end=' ')
        for process in processes_to_benchmark:
            print(process.name(), end=' ')
        print()

        last_time_monitored = time.time()

    # our wrapper exited, and no simkaMerge is hanging around, so end
        
        
    walltime_end = time.time()

    # write the stats to the output file
    with open(output_file, 'w') as f:
        f.write(f'Peak memory usage (bytes): {peak_memory}\n')
        f.write(f'Total CPU time (seconds): {total_cpu_time}\n')
        f.write(f'Walltime (seconds): {walltime_end - walltime_start}\n')

    print('**********************************')
    print('EXITING MONITOR SCRIPT')
    print('**********************************')



if __name__ == "__main__":
    # the first command line argument is the pid of the process to monitor
    # the second command line argument is the output filename
    # e.g. python main.py 1234 resources
    # if no pid is provided, the script will exit
    if len(os.sys.argv) < 3:
        os.sys.exit(1)

    # check first argument is a valid integer
    try:
        int(os.sys.argv[1])
    except ValueError:
        os.sys.exit(1)

    # check second argument is a valid string
    try:
        str(os.sys.argv[2])
    except ValueError:
        os.sys.exit(1)

    pid_to_monitor = int(os.sys.argv[1])
    output_file = str(os.sys.argv[2])
    main(pid_to_monitor, output_file)