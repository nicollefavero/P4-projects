#!/usr/bin/env python3
import pexpect
import argparse
import subprocess
import sys
import os
import time
import datetime

MAKEFILE_PATH = "/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/3-Endpoints/QUIC-Tr4ck/p4-src/Makefile"
SCRIPTS_PATH = "/home/p4/Repositories/P4-projects/QUIC-Tr4ck-Impl/3-Endpoints/QUIC-Tr4ck"

def generate_request_time_log(output_dir, times, interval, num_requests, burst_size, burst_interval, burst_count):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    file_name = f"{output_dir}/r{num_requests}-i{interval}-s{burst_size}-c{burst_count}-t{burst_interval}".replace(".", "_")

    with open(f"{file_name}.log", "w") as file:
        for time in times:
            file.write(str(time))
            file.write("\n")


class MininetProc:
    def __init__(self) -> None:
        self.proc = pexpect.spawn("make run", cwd=os.path.dirname(MAKEFILE_PATH), encoding="utf-8")
        self.proc.logfile_read = sys.stdout

    def run_server(self, logs=False, output_folder=None):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h2 python3 {SCRIPTS_PATH}/quic-src/receive.py --certificate {SCRIPTS_PATH}/quic-src/tests/ssl_cert.pem --private-key {SCRIPTS_PATH}/quic-src/tests/ssl_key.pem &")

        if logs:
            self.proc.expect("mininet> ", timeout=None)
            self.proc.sendline(f"h2 python3 {SCRIPTS_PATH}/generate-server-logs.py -o {output_folder}/baseline -p \"$(jobs -l)\" &")


    def run_client(self, interval, num_requests):
        self.proc.expect("mininet> ", timeout=None)

        conn_times = []
        for i in range(num_requests):
            t_start = time.time()
            self.proc.sendline(f"h3 {SCRIPTS_PATH}/quic-src/python3 send.py --ca-certs tests/pycacert.pem https://10.0.2.2:4433/")
            t_end = time.time()

            conn_times.append(t_end - t_start)
            time.sleep(interval)

        return conn_times


    def run_server_logs(self, output_folder):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h2 python3 {SCRIPTS_PATH}/generate-server-logs.py -o {output_folder} -p \"$(jobs -l)\" &")


    def run_attack(self, burst_size, burst_interval, burst_count, logs=False, output_folder=None):
        if logs:
            self.run_server_logs(f"{output_folder}/s{burst_size}-c{burst_count}-t{burst_interval}".replace(".", "_"))

        time.sleep(3)
        # quantos bursts espacados por tempo (x segundos)
        for j in range(0, burst_count):
            # burst de pacotes (grupo de pacotes por vez)
            for i in range(0, burst_size):
                self.proc.sendline(f"h1 python3 {SCRIPTS_PATH}/quic-src/send.py --ca-certs {SCRIPTS_PATH}/quic-src/tests/pycacert.pem https://10.0.2.2:4433/ &")
            time.sleep(burst_interval)

        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline(f"h1 python3 {SCRIPTS_PATH}/quic-src/send.py --ca-certs {SCRIPTS_PATH}/quic-src/tests/pycacert.pem https://10.0.2.2:4433/")

    def exit(self):
        self.proc.expect("mininet> ", timeout=None)
        self.proc.sendline("exit")

def clean():
    subprocess.run(["make", "clean"], cwd=os.path.dirname(MAKEFILE_PATH))

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--burst-size", type=int, default=0)
    parser.add_argument("-c", "--burst-count", type=int, default=0)
    parser.add_argument("-t", "--burst-interval", type=float, default=0)
    parser.add_argument("-r", "--requests-number", type=int, default=1)
    parser.add_argument("-i", "--interval", type=int, default=0)
    parser.add_argument("-o", "--output-folder", type=str, default=f"{SCRIPTS_PATH}/server-logs")
    parser.add_argument("-d", "--output-dir", type=str, default=f"{SCRIPTS_PATH}/client-logs")
    return parser.parse_args()

def main():
    args = get_args()
    burst_size = args.burst_size    # workload size
    burst_count = args.burst_count
    burst_interval = args.burst_interval
    output_folder = args.output_folder
    num_requests = args.requests_number
    interval = args.interval
    output_client = args.output_dir

    clean()
    mininet_proc = MininetProc()

    if burst_size > 0:
        mininet_proc.run_server()
        time.sleep(2)
        mininet_proc.run_attack(burst_size, burst_interval, burst_count)
        conn_times = mininet_proc.run_client(interval, num_requests)
        generate_request_time_log(output_client, conn_times, interval, num_requests, burst_size, burst_interval, burst_count)
    else:
        mininet_proc.run_server(logs=True)

    mininet_proc.exit()

if __name__ == "__main__":
    main()
